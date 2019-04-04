import ast
from collections import namedtuple

Import = namedtuple('Import', ['module', 'name', 'alias'])
Class = namedtuple('Class', ['node', 'name'])
Method = namedtuple('Method', ['node', 'name', 'docstring'])


def get_imports(root):
    for node in ast.iter_child_nodes(root):
        if isinstance(node, ast.Import):
            module = []
        elif isinstance(node, ast.ImportFrom):
            module = node.module
        else:
            continue

        for name in node.names:
            yield Import(module, name.name, name.asname)


def get_classes(root):
    for node in ast.iter_child_nodes(root):
        if isinstance(node, ast.ClassDef):
            yield Class(node, node.name)


def get_functions(root):
    for node in ast.iter_child_nodes(root):
        if isinstance(node, ast.FunctionDef):
            yield Method(node, node.name, ast.get_docstring(node))


def parse_file(file_content):
    return ast.parse(file_content)
