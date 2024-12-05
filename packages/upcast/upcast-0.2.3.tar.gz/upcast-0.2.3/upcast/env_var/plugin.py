from typing import ClassVar, Optional

from ast_grep_py import Range, SgNode
from pydantic import Field

from upcast.env_var.core import Context, EnvVar, Plugin, PluginHub, PYVar
from upcast.utils import FunctionArgs


class ModuleImportPlugin(Plugin):
    priority: int = 2

    def handle_import(self, context: Context, node: SgNode) -> bool:
        result = node.find(pattern="import $MODULE")
        if not result:
            return False

        module_node = result.get_match("MODULE")
        context.add_module(module_node.text())

    def handle_import_from(self, context: Context, node: SgNode):
        result = node.find_all(pattern="from $MODULE import $$$NAME")
        for i in result:
            module_node = i.get_match("MODULE")
            module_name = module_node.text()

            for name_node in i.get_multiple_matches("NAME"):
                if name_node.kind() == ",":
                    continue

                context.add_imports(module_name, name_node.text())

    def handle(self, context: Context, node: SgNode):
        self.handle_import(context, node)
        self.handle_import_from(context, node)


class PyVarPlugin(Plugin):
    priority: int = 2

    def handle(self, context: Context, node: SgNode):
        assign_nodes = node.find_all(pattern="$NAME = $VALUE")
        for i in assign_nodes:
            name_node = i["NAME"]
            name_node_range = name_node.range()
            if name_node_range.start.column != 0:
                continue

            value_node = i["VALUE"]
            if value_node.kind() == "call":
                continue

            try:
                value = context.evalidate_node(value_node)
            except Exception:
                continue

            context.add_global_var(PYVar(name=name_node.text(), node=i, value=value))


class FixMixin:
    value_kind_to_cast_mappings: ClassVar[dict[str, str]] = {
        "string": "str",
        "integer": "int",
        "float": "float",
        "true": "bool",
        "false": "bool",
        "list": "list",
        "tuple": "tuple",
        "dictionary": "dictionary",
    }

    def handle_name(self, context: Context, node: Optional[SgNode]) -> (str, Range):
        if not node:
            return ""

        node_kind = node.kind()
        if node_kind not in ["string", "binary_operator"]:
            return ""

        try:
            return context.evalidate_node(node)
        except Exception:
            return node.text()

    def handle_value(
        self,
        context: Context,
        cast_node: Optional[SgNode],
        value_node: Optional[SgNode],
    ) -> (str, str):
        cast = ""
        if cast_node and cast_node.matches(kind="identifier"):
            cast = cast_node.text()

        if not value_node:
            return cast, ""

        if not cast and value_node.kind() in self.value_kind_to_cast_mappings:
            cast = self.value_kind_to_cast_mappings[value_node.kind()]

        return cast, value_node.text()

    def make_env_var(
        self,
        context: Context,
        result: SgNode,
        required: bool,
    ) -> Optional[EnvVar]:
        name_node = result.get_match("NAME")
        if not name_node:
            return None

        name = self.handle_name(context, name_node)
        if not name:
            return None

        cast, value = self.handle_value(
            context, result.get_match("TYPE"), result.get_match("VALUE")
        )

        name_node_range = name_node.range()

        return EnvVar(
            node=result,
            name=name,
            value=value,
            cast=cast,
            required=required,
            position=(name_node_range.start.line + 1, name_node_range.start.column + 1),
        )


class EnvRefPlugin(Plugin, FixMixin):
    pattern: str
    module: str = ""
    imports: str = ""
    type_convert: bool = True
    or_default: bool = True
    required: bool = False
    priority: int = 8

    @property
    def patterns(self) -> list[str]:
        yield self.pattern

        if self.type_convert and self.or_default:
            yield f"$TYPE({self.pattern}) or $VALUE"
            yield f"$TYPE({self.pattern} or $VALUE)"

        if self.type_convert:
            yield f"$TYPE({self.pattern})"

        if self.or_default:
            yield f"{self.pattern} or $VALUE"

    def should_run(self, context: Context, node: SgNode) -> bool:
        return context.has_imports(self.module, self.imports)

    def iter_var_by_pattern(self, context: Context, pattern: str, node: SgNode):
        for i in node.find_all(pattern=pattern):
            env_var = self.make_env_var(context, i, self.required)
            if env_var:
                yield env_var

    def handle(self, context: Context, node: SgNode):
        for pattern in self.patterns:
            for i in self.iter_var_by_pattern(context, pattern, node):
                context.add_env_var(i)


class DjangoEnvPlugin(EnvRefPlugin, FixMixin):
    pattern: str = ""
    priority: int = 7
    var_class: str = "Env"
    var_name: str = "env"
    defined_vars: set[str] = Field(default_factory=set)

    @property
    def patterns(self) -> list[str]:
        yield f"{self.var_name}.$TYPE($NAME)"
        yield f"{self.var_name}($NAME)"
        yield f"{self.var_name}.$TYPE($NAME, default=$VALUE)"
        yield f"{self.var_name}.$TYPE($NAME, $VALUE)"

    def should_run(self, context: Context, node: SgNode) -> bool:
        if context.has_module("environ"):
            self.var_class = "environ.Env"

            return True

        return bool(context.has_imports("environ", "Env"))

    def handle_declare(self, context: Context, node: SgNode) -> str:
        declare_node = node.find(pattern=f"$NAME = {self.var_class}($$$ARGS)")
        if not declare_node:
            return self.var_name

        self.var_name = declare_node["NAME"].text()
        args = FunctionArgs().parse(declare_node, "ARGS")

        for name, arg in args.args.items():
            arg_node = arg.value_node
            cast_node = arg_node.child(1)
            value_node = arg_node.child(3)
            name_node_range = arg.node.range()

            self.defined_vars.add(name)
            context.add_env_var(
                EnvVar(
                    node=arg.node,
                    name=name,
                    value=value_node.text(),
                    cast=cast_node.text(),
                    position=(
                        name_node_range.start.line + 1,
                        name_node_range.start.column + 1,
                    ),
                )
            )

    def handle(self, context: Context, node: SgNode):
        self.handle_declare(context, node)
        for pattern in self.patterns:
            for i in self.iter_var_by_pattern(context, pattern, node):
                if not i.value and i.name not in self.defined_vars:
                    i.required = True

                context.add_env_var(i)


class EnvVarHub(PluginHub):
    django_env_name: str = "env"
    additional_required_patterns: list[str] = Field(default_factory=list)
    additional_patterns: list[str] = Field(default_factory=list)

    @property
    def plugins(self) -> list[Plugin]:
        p = [
            ModuleImportPlugin(),
            PyVarPlugin(),
            # stdlib
            EnvRefPlugin(pattern="os.getenv($NAME)", module="os"),
            EnvRefPlugin(pattern="os.getenv($NAME, $VALUE)", module="os"),
            EnvRefPlugin(pattern="os.environ[$NAME]", module="os", required=True),
            EnvRefPlugin(pattern="os.environ.get($NAME)", module="os"),
            EnvRefPlugin(pattern="os.environ.get($NAME, $VALUE)", module="os"),
            EnvRefPlugin(pattern="getenv($NAME)", module="os", imports="getenv"),
            EnvRefPlugin(
                pattern="getenv($NAME, $VALUE)", module="os", imports="getenv"
            ),
            EnvRefPlugin(
                pattern="environ[$NAME]", module="os", imports="environ", required=True
            ),
            EnvRefPlugin(pattern="environ.get($NAME)", module="os", imports="environ"),
            EnvRefPlugin(
                pattern="environ.get($NAME, $VALUE)", module="os", imports="environ"
            ),
            # django env
            DjangoEnvPlugin(),
        ]

        for i in self.additional_required_patterns:
            p.append(EnvRefPlugin(pattern=i, required=True, priority=10))

        for i in self.additional_patterns:
            p.append(EnvRefPlugin(pattern=i, priority=10))

        return p
