import ast
import glob
import os
from collections import namedtuple

from kojak.exceptions import KojakException

Import = namedtuple('Import', ['module', 'name', 'alias'])
Class = namedtuple('Class', ['node', 'name'])
Method = namedtuple('Method', ['node', 'name', 'docstring'])


class Module:
    count_imports = 0
    count_classes = 0

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
            raise KojakException("Invalid python file {filename}".format(
                filename=self.name))

    def get_imports(self):
        for node in ast.iter_child_nodes(self.root):
            if isinstance(node, ast.Import):
                module = []
            elif isinstance(node, ast.ImportFrom):
                module = node.module
            else:
                continue

            for name in node.names:
                self.count_imports += 1
                yield Import(module, name.name, name.asname)

    def get_classes(self):
        for node in ast.iter_child_nodes(self.root):
            if isinstance(node, ast.ClassDef):
                self.count_classes += 1
                yield Class(node, node.name)

    def get_functions(self, root=None):
        root = root if root else self.root

        for node in ast.iter_child_nodes(root):
            if isinstance(node, ast.FunctionDef):
                yield Method(node, node.name, ast.get_docstring(node))


class Analyze(object):
    """To analyze the file."""

    def __init__(self, path):
        """To initalize the analyze class.

        @param path: The path of the file or directory to analyze
        @type path: str
        """
        self.path = path
        self.modules = []
        if os.path.isfile(self.path):
            with open(self.path, 'r') as pyfile:
                self.modules.append(Module(pyfile))
        elif os.path.isdir(self.path):
            for pyfile in glob.glob('{path}/**/*.py'.format(path=self.path),
                                    recursive=True):
                with open(pyfile) as module:
                    self.modules.append(Module(module))
        else:
            raise KojakException("Path not found: {path}".format(path=path))

    def get_modules(self):
        """Retrieve modules."""
        for module in self.modules:
            yield module

    def get_global_stats(self):
        """Retrieve global stats of the analyze."""
        imports = 0
        classes = 0
        modules = len(self.modules)
        for module in self.modules:
            [el for el in module.get_classes()]
            [el for el in module.get_imports()]
            imports += module.count_imports
            classes += module.count_classes
        return {"imports": imports, "classes": classes, "modules": modules}
