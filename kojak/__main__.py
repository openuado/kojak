import argparse
from sys import exit

from kojak.utils import Analyze


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

    analyze = Analyze(filename)
    all_import = []

    for imp in analyze.get_imports():
        result = ''

        if imp.module:
            result = 'From {module} import {name}'.format(
                module=imp.module, name=imp.name)

        if not imp.module:
            result = 'Import {name}'.format(name=imp.name)

        if imp.alias:
            result += ' with an alias {alias}'.format(alias=imp.alias)

        all_import.append('\t-{result}'.format(result=result))

    print('This module {module} contains {count} imports'.format(
        module=analyze.path.name, count=analyze.count_imports))
    print('\n'.join(all_import))

    all_class = {}
    for cls in analyze.get_classes():
        all_class[cls.name] = []

        for func in analyze.get_functions(cls.node):
            all_class[cls.name].append('\t\t-{name}'.format(name=func.name))

    word_class = 'class' \
        if analyze.count_classes == 1 else 'classes'
    print('This module contains {count} {word_class}:'.format(
        count=analyze.count_classes, word_class=word_class))

    for key, value in all_class.items():
        print('\t-{name}'.format(name=key))
        print('\n'.join(value))

    if analyze.count_classes == 0:
        print("This module {module} doesn't contains class.".format(
            module=analyze.path.name))


if __name__ == "__main__":
    exit(main())
