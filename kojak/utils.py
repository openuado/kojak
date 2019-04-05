import ast
from collections import namedtuple

Import = namedtuple('Import', ['module', 'name', 'alias'])
Class = namedtuple('Class', ['node', 'name'])
Method = namedtuple('Method', ['node', 'name', 'docstring'])


class Analyze(object):
    """To analyze the file."""

    count_imports = 0
    count_classes = 0

    def __init__(self, path):
        """To initalize the analyze class.

        @param path: The path of the file or directory to analyze
        @type path: str
        """
        self.path = path
        self.root = ast.parse(self.path.read())

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
