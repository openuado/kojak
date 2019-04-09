import ast
import os
from collections import namedtuple

from kojak.common import python_files
from kojak.exceptions import KojakException

Import = namedtuple("Import", ["module", "name", "alias"])
Class = namedtuple("Class", ["node", "name", "methods"])
Method = namedtuple("Method", ["node", "name", "docstring"])


def get_functions(root):
    funcs = []
    for node in ast.iter_child_nodes(root):
        if isinstance(node, ast.FunctionDef):
            funcs.append(Method(node, node.name, ast.get_docstring(node)))
    return funcs


class Classes(list):
    def __init__(self, root):
        """Initialize list of classes."""
        super(Classes, self).__init__()
        for node in ast.iter_child_nodes(root):
            if isinstance(node, ast.ClassDef):
                meths = get_functions(node)
                self.append(Class(node, node.name, meths))

    def __str__(self):
        """Textual representation of classes."""
        return "\n".join(self.name)


class Imports(list):
    def __init__(self, root):
        """Initialize list of imports."""
        super(Imports, self).__init__()
        for node in ast.iter_child_nodes(root):
            if isinstance(node, ast.Import):
                module = []
            elif isinstance(node, ast.ImportFrom):
                module = node.module
            else:
                continue

            for name in node.names:
                self.append(Import(module, name.name, name.asname))

    def __str__(self):
        """Textual representation of imports."""
        return "\n".join(self.name)


class Module:
    def __init__(self, path):
        """To initalize the analyze class.

        @param path: The path of the file or directory to analyze
        @type path: str
        """
        self.path = path
        self.name = path.name
        try:
            self.root = ast.parse(self.path.read())
        except SyntaxError:
            raise KojakException(
                "Invalid python file {filename}".format(filename=self.name)
            )
        self.imports = Imports(self.root)
        self.classes = Classes(self.root)

    def __str__(self):
        """Textual representation of module."""
        return self.name


class Analyze(object):
    """To analyze the file."""

    modules = []
    imports = 0
    classes = 0

    def __init__(self, path):
        """To initalize the analyze class.

        @param path: The path of the file or directory to analyze
        @type path: str
        """
        self.path = path
        self.modules = []
        if os.path.isfile(self.path):
            with open(self.path, "r") as pyfile:
                self.modules.append(Module(pyfile))
        elif os.path.isdir(self.path):
            for module in python_files(self.path):
                with open(module, "r") as pyfile:
                    current_module = Module(pyfile)
                    self.modules.append(current_module)
        else:
            raise KojakException("Path not found: {path}".format(path=path))
        self._count_imports()
        self._count_classes()

    def _count_imports(self):
        for module in self.modules:
            self.imports += len(module.imports)

    def _count_classes(self):
        for module in self.modules:
            self.classes += len(module.classes)
