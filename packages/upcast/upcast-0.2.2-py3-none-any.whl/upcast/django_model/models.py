import os.path
from collections import Counter, defaultdict
from typing import Any, Optional

from ast_grep_py import SgNode
from pydantic import BaseModel, Field


class ModelField(BaseModel):
    node: SgNode = Field(title="Node of the field", exclude=True)
    name: str = Field("", title="Name of the field")
    type: str = Field("", title="Type of the field")
    class_path: str = Field("", title="Class path of the field")
    kwargs: dict[str, Any] = Field(default_factory=dict, title="Keyword arguments")

    class Config:
        arbitrary_types_allowed = True


class ModelIndex(BaseModel):
    node: SgNode = Field(title="Node of the index", exclude=True)
    fields: list[str] = Field(default_factory=list, title="Fields of the index")
    kind: str = Field("", title="Kind of the index")

    class Config:
        arbitrary_types_allowed = True


class ModelBase(BaseModel):
    node: SgNode = Field(title="Node of the model", exclude=True)
    name: str = Field("", title="Name of the model")
    class_path: str = Field("", title="Class path of the model")

    class Config:
        arbitrary_types_allowed = True


class ModelMethod(BaseModel):
    node: SgNode = Field(title="Node of the method", exclude=True)
    name: str = Field("", title="Name of the method")
    args: int = Field(0, title="Number of arguments")
    lines: int = Field(0, title="Number of lines")

    class Config:
        arbitrary_types_allowed = True


class ModelMeta(BaseModel):
    node: SgNode = Field(title="Node of the model", exclude=True)
    abstract: bool = Field(False, title="Abstract model")
    app_label: str = Field("", title="App label")
    db_table: str = Field("", title="Database table")
    managed: bool = Field(True, title="Managed model")
    proxy: bool = Field(False, title="Proxy model")
    verbose_name: str = Field("", title="Verbose name")
    verbose_name_plural: str = Field("", title="Verbose name plural")

    class Config:
        arbitrary_types_allowed = True


class Model(BaseModel):
    node: SgNode = Field(title="Node of the model", exclude=True)
    name: str = Field(title="Name of the model")
    file: str = Field(title="Path of the file")
    locations: list[str] = Field(default_factory=list, title="Modules of the model")
    position: tuple[int, int] = Field(title="Position of the model")
    weight: int = Field(0, title="Weight of model")
    lines: int = Field(0, title="Number of lines")
    bases: list[ModelBase] = Field(default_factory=list, title="Base classes of the model")
    fields: list[ModelField] = Field(default_factory=list, title="Fields of the model")
    indexes: list[ModelIndex] = Field(default_factory=list, title="Indexes of the model")
    methods: list[ModelMethod] = Field(default_factory=list, title="Methods of the model")
    manager: str = Field("", title="Manager of the model")
    meta: Optional[ModelMeta] = Field(default=None, title="Meta of the model")

    class Config:
        arbitrary_types_allowed = True


class ImportedModule(BaseModel):
    module: str = Field("", title="Module name")
    name: str = Field("", title="Name of the class")
    alias: str = Field("", title="Alias of the class")

    def real_name(self):
        return self.alias or self.name


class Context(BaseModel):
    root_dir: str = Field(title="Root directory")
    module: str = Field("", title="Module name")
    current_file: str = Field("", title="Current file")
    resolved_models: dict[str, Model] = Field(default_factory=dict, title="Resolved models")
    unresolved_models: list[Model] = Field(default_factory=list, title="Unresolved models")
    module_imports: dict[str, ImportedModule] = Field(default_factory=dict, title="Imported models")
    module_refs: dict[str, dict[str, ImportedModule]] = Field(
        default_factory=lambda: defaultdict(dict), title="Module references"
    )
    weight: Counter[str] = Field(default_factory=Counter, title="Model weight")

    class Config:
        arbitrary_types_allowed = True

    def switch_to_file(self, file: str):
        self.current_file = file if file else ""
        self.module = self.file_to_module(file)
        self.module_imports = {}

    def reset(self):
        self.switch_to_file("")

    def add_imported_module(self, module: ImportedModule, export: bool = False):
        self.module_imports[module.real_name()] = module

        if export:
            self.module_refs[module.module][module.name] = ImportedModule(
                module=self.module,
                name=module.name,
                alias=module.alias,
            )

    def file_to_module(self, file: str) -> str:
        if not file:
            return ""

        relpath = os.path.relpath(file, self.root_dir)
        path, file = os.path.split(relpath)

        if file == "__init__.py":
            pass
        elif "." not in file:
            path = relpath
        else:
            path, _ = os.path.splitext(relpath)

        return path.replace(os.path.sep, ".")

    def get_module_path(self, path: str) -> str:
        imported, _, attribute = path.partition(".")
        module = self.module_imports.get(imported)
        if module:
            return f"{module.module}.{path}"

        return f"{self.module}.{path}"

    def split_module_path(self, path: str) -> tuple[str, str]:
        path, sep, name = path.rpartition(".")
        if sep:
            return path, name

        return "", path

    def get_models(self) -> list[Model]:
        models: dict[int, Model] = {}

        for i in self.resolved_models.values():
            models[id(i)] = i

        for i in self.unresolved_models:
            models[id(i)] = i

        return sorted(models.values(), key=lambda i: (-i.weight, -i.lines, i.name))
