import argparse
from sys import exit

from kojak.utils import get_classes, get_functions, get_imports, parse_file


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

    analyze = parse_file(filename.read())

    print('List imports by the module:')
    for imp in get_imports(analyze):
        result = ''

        if imp.module:
            result = 'From {module} import {name}'.format(
                module=imp.module, name=imp.name)

        if not imp.module:
            result = 'Import {name}'.format(name=imp.name)

        if imp.alias:
            result += ' with an alias {alias}'.format(alias=imp.alias)

        print('\t-{result}'.format(result=result))

    for cls in get_classes(analyze):
        print('List classes by the module:')
        print(cls.name)

        for func in get_functions(cls.node):
            print('\t-{}'.format(func.name))


if __name__ == "__main__":
    exit(main())
