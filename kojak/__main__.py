import argparse
import ast
from sys import exit


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
    for cls in classes:
        print(cls)
        for meth in classes[cls]:
            print('\t-{}'.format(meth))


if __name__ == "__main__":
    exit(main())
