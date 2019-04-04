import argparse
import ast
from collections import namedtuple
from sys import exit


def _get_import(root):
    Import = namedtuple('Import', ['module', 'name', 'alias'])

    for node in ast.iter_child_nodes(root):
        if isinstance(node, ast.Import):
            module = []
        elif isinstance(node, ast.ImportFrom):
            module = node.module
        else:
            continue

        for name in node.names:
            yield Import(module, name.name, name.asname)


def argparser():
    parser = argparse.ArgumentParser(description='Analyze python file')
    parser.add_argument('file', nargs='?', type=argparse.FileType(),
                        help="Path to analyze. \
                        If not provided kojak read from stdin")
    parser.add_argument('-o', '--object', type=str,
                        help="output format")
    return parser.parse_args()


def main():
    args = argparser()
    filename = args.file
    if not filename:
        return 0

    classes = {}
    functions = []
    analyze = ast.parse(filename.read())

    for node in analyze.body:
        if 'lineno' not in dir(node) or 'col_offset' not in dir(node):
            continue
        if type(node) is ast.FunctionDef:
            functions.append(node.name)
        elif type(node) is ast.ClassDef:
            classes.update({node.name: []})
            for member in node.body:
                if type(member) is ast.FunctionDef:
                    classes[node.name].append(member.name)

    print('List import by the module:')
    for imp in _get_import(analyze):
        result = ''

        if imp.module:
            result = 'From {module} import {name}'.format(
                module=imp.module, name=imp.name)

        if not imp.module:
            result = 'Import {name}'.format(name=imp.name)

        if imp.alias:
            result += ' with an alias {alias}'.format(alias=imp.alias)

        print('\t-{result}'.format(result=result))

    for cls in classes:
        print('List classes by the module:')
        print(cls)

        for meth in classes[cls]:
            print('\t-{}'.format(meth))


if __name__ == "__main__":
    exit(main())
