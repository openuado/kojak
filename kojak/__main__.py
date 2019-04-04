import argparse
from sys import exit

import kojak


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

    analyze = kojak.parse_file(filename.read())

    print('List import by the module:')
    for imp in kojak.get_import(analyze):
        result = ''

        if imp.module:
            result = 'From {module} import {name}'.format(
                module=imp.module, name=imp.name)

        if not imp.module:
            result = 'Import {name}'.format(name=imp.name)

        if imp.alias:
            result += ' with an alias {alias}'.format(alias=imp.alias)

        print('\t-{result}'.format(result=result))

    for cls in kojak.get_classes(analyze):
        print('List classes by the module:')
        print(cls.name)

        for func in kojak.get_functions(cls.node):
            print('\t-{}'.format(func.name))


if __name__ == "__main__":
    exit(main())
