import os


def _or_default(obj, default):
    return default if obj is None else obj


def _to_nameable_dict(nameable: list["Nameable"]) -> dict[str, "Nameable"]:
    nameable = _or_default(nameable, [])
    if not isinstance(nameable, list) and isinstance(nameable, tuple):
        nameable = list(nameable)
    values = {}
    for param in nameable:
        values[param.name] = param

    return values


_INDENTATION = "    "


class Nameable:
    def __init__(self, name: str):
        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = str(name)

    def __str__(self):
        return self.name


class Indenteable:
    def __init__(self, level: int):
        self._level = level

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, level: int):
        level = int(_or_default(level, 0))
        if level < 0:
            level = 0
        self._level = level

    @property
    def indent(self):
        return (self.level - 1) * _INDENTATION

    @property
    def next_indent(self):
        return (self.level + 1) * _INDENTATION


class PyVariable(Nameable, Indenteable):
    def __init__(self, name: str, level: int = 0, value=None, has_value: bool = False):
        Nameable.__init__(self, name)
        Indenteable.__init__(self, level)
        if value is not None:
            has_value = True
        self.value = value
        self.has_value = has_value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: str):
        if value is None:
            _val = "None"
        else:
            _val = str(value)
        self._value = _val

    @property
    def has_value(self):
        return self.__has_value

    @has_value.setter
    def has_value(self, has_default):
        self.__has_value = has_default

    def __str__(self):
        return self.indent + self.name + " = " + self.value


class PyParameter(PyVariable):
    def __init__(self, name: str, value=None, has_value: bool = False):
        super().__init__(name, 0, value, has_value)

    def __str__(self):
        if not self.has_value:
            return self.name
        return self.name + "=" + self.value


class PyFunction(Nameable, Indenteable):
    def __init__(self, name: str, params: list[PyParameter] = None, level: int = 0,
                 return_type: str = None, simple_return: str = None):
        Nameable.__init__(self, name)
        Indenteable.__init__(self, level)
        self.parameters = params
        self.return_type = return_type
        self.simple_return = simple_return

    @property
    def parameters(self):
        return self.__params

    @parameters.setter
    def parameters(self, params: list[PyParameter]):
        self.__params = _to_nameable_dict(params)

    @property
    def return_type(self):
        return self.__return_type

    @return_type.setter
    def return_type(self, return_type: str):
        if return_type is None:
            self.__return_type = None
        else:
            self.__return_type = str(return_type)

    @property
    def simple_return(self):
        return self.__simple_return

    @simple_return.setter
    def simple_return(self, simple_return: str):
        self.__simple_return = str(_or_default(simple_return, ""))

    def __str__(self):
        out = self.indent + "def " + self.name.strip() + "("
        if self.parameters:
            out += ", ".join(str(param) for param in self.parameters.values())

        end = ")"
        if self.return_type:
            end += " -> " + self.return_type
        end += ":\n" + self.next_indent

        end += "return " + self.simple_return if self.simple_return else "pass"

        out += end
        return out


class PyClass(Nameable, Indenteable):
    def __init__(self, name: str, parent: Nameable = None, methods: list[PyFunction] = None, level: int = 0):
        Nameable.__init__(self, name)
        Indenteable.__init__(self, level)
        self.methods = methods
        self.__parent = None
        self.parent = parent

    @property
    def methods(self) -> dict[str, PyFunction]:
        return self.__methods

    @methods.setter
    def methods(self, methods: list[PyFunction]):
        self.__methods = _to_nameable_dict(methods)

    @property
    def parent(self):
        return self.__parent

    @parent.setter
    def parent(self, parent: Nameable):
        if parent is None:
            self.__parent = None
        elif parent:
            parent = str(parent)
            if self.__parent is None:
                self.__parent = Nameable(parent)
            else:
                self.__parent.name = parent

    def __str__(self):
        parent = ""

        if self.parent:
            parent = "(" + str(self.parent) + ")"

        out = self.indent + "class " + self.name.strip() + parent + ":\n"
        next_indent = self.next_indent
        if self.methods:
            def check_method(method: PyFunction):
                if method.level <= self.level:
                    method.level = self.level + 1
                if method.parameters:
                    method.parameters = [PyParameter("self"), ] + list(method.parameters.values())
                else:
                    method.parameters = [PyParameter("self")]
                return method

            methods = map(check_method, self.methods.values())

            out += next_indent + ("\n\n" + next_indent).join(str(method) for method in methods)
        else:
            out += next_indent + "pass"

        return out


class PyImport:
    def __init__(self, package: Nameable, imports: list[Nameable] = None,
                 import_all: bool = False, relative: bool = False):
        self.__package = package
        if not imports:
            imports = []
        self.__imports = tuple(imports)
        self.__import_all = import_all
        self.__relative = relative

    def __str__(self):
        def get_imports():
            if self.__imports:
                return ", ".join(str(it) for it in self.__imports)
            return ""

        if self.__relative:
            if self.__import_all:
                return "from .{} import *".format(self.__package)
            elif self.__imports:
                return "from .{} import {}".format(self.__package, get_imports())

            return "from . {}".format(self.__package)
        elif self.__imports:
            return "from {} import {}".format(self.__package, get_imports())
        elif self.__import_all:
            return "from {} import *".format(self.__package)

        return "import {}".format(self.__package)


class PyFile(Nameable):
    def __init__(self, name: str, functions: list[PyFunction] = None, classes: list[PyClass] = None,
                 variables: list[PyVariable] = None, imports: list[PyImport] = None):
        super().__init__(name)
        self.functions = functions
        self.classes = classes
        self.variables = variables
        self.imports = imports

    @property
    def functions(self):
        return self.__functions

    @functions.setter
    def functions(self, functions: list[PyFunction]):
        self.__functions = _to_nameable_dict(functions)

    @property
    def classes(self):
        return self.__classes

    @classes.setter
    def classes(self, classes: list[PyClass]):
        self.__classes = _to_nameable_dict(classes)

    @property
    def variables(self) -> dict[str, PyVariable]:
        return self.__vars

    @variables.setter
    def variables(self, variables: list[PyVariable]):
        self.__vars = _to_nameable_dict(variables)

    @property
    def imports(self) -> tuple[str]:
        return self.__imports

    @imports.setter
    def imports(self, imports: list[str]):
        imports = _or_default(imports, [])
        if not isinstance(imports, list) and isinstance(imports, tuple):
            imports = list(imports)
        self.__imports = tuple(imports)

    def _get_file_data(self):
        data = ""
        if self.imports:
            data += "\n".join(str(item) for item in self.imports)
            data += "\n\n\n"

        if self.classes:
            data += "\n\n\n".join(str(item) for item in self.classes.values())
            data += "\n\n"
        if self.functions:
            data += "\n\n\n".join(str(item) for item in self.functions.values())

        if self.variables:
            data += "\n".join(str(item) for item in self.variables.values())
            data += "\n\n"

        return data

    def create(self, folder: str = None):
        path = self.name + ".py"
        if folder:
            path = os.path.join(str(folder), path)

        with open(path, "w", encoding="utf-8") as fs:
            data = self._get_file_data()
            fs.write(data)


class PyPackage(PyFile):
    def __init__(self, name: str, files: list[PyFile] = None, packages: list["PyPackage"] = None,
                 functions: list[PyFunction] = None, classes: list[PyClass] = None,
                 variables: list[PyVariable] = None, import_all: bool = False, imports: list[PyImport] = None):
        super().__init__(name, functions=functions, classes=classes, variables=variables, imports=imports)
        self.files = files
        self.packages = packages
        self.import_all = import_all

    @property
    def files(self) -> dict[str, PyFile]:
        return self.__files

    @files.setter
    def files(self, files: list[PyFile]):
        self.__files = _to_nameable_dict(files)

    @property
    def packages(self) -> dict[str, "PyPackage"]:
        return self.__packages

    @packages.setter
    def packages(self, packages: list["PyPackage"]):
        self.__packages = _to_nameable_dict(packages)

    @property
    def import_all(self):
        return self.__import_all

    @import_all.setter
    def import_all(self, import_all: bool):
        self.__import_all = _or_default(import_all, False)

    def create(self, folder: str = None):
        path = self.name
        if folder:
            path = os.path.join(str(folder), path)

        os.makedirs(path, exist_ok=True)

        def __get_import(nameable: Nameable):
            if self.import_all:
                return "from ." + nameable.name + " import *"
            return "from . import " + nameable.name

        imports_all = ""
        if self.files:
            for file in self.files.values():
                file.create(path)
                imports_all += __get_import(file) + "\n"

        if self.packages:
            for package in self.packages.values():
                package.create(path)
                imports_all += __get_import(package) + "\n"

        path = os.path.join(path, "__init__.py")
        with open(path, "w", encoding="utf-8") as fs:
            data = ""
            if imports_all:
                data += imports_all + "\n\n"

            data += self._get_file_data()
            fs.write(data)
