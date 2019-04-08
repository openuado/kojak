import argparse
import os
import sys

from kojak.common import is_valid_path, pluralize


class readable_path(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        try:
            is_valid_path(values)
        except (IOError, OSError) as err:
            print(str(err))
            parser.print_help()
            sys.exit(1)
        else:
            setattr(namespace, self.dest, values)


def argparser():
    parser = argparse.ArgumentParser(description='Analyze python file')
    parser.add_argument('file', nargs='?', action=readable_path,
                        help="Path to analyze. \
                        If not provided kojak analyze the current working dir",
                        default=os.getcwd())
    parser.add_argument('-s', '--summarize', action='store_true',
                        help='If display a summary of the analyze')
    parser.add_argument('-V', '--version', action='store_true',
                        help='Only display the kojak version number')
    return parser.parse_args()


def imports(module):
    all_import = []
    for imp in module.get_imports():
        result = ''

        if imp.module:
            result = 'From {module} import {name}'.format(
                module=imp.module, name=imp.name)

        if not imp.module:
            result = 'Import {name}'.format(name=imp.name)

        if imp.alias:
            result += ' with an alias {alias}'.format(alias=imp.alias)

        all_import.append('\t-{result}'.format(result=result))

    print('This module {module} contains {count} {word_imports}'.format(
        module=module.path.name,
        count=module.count_imports,
        word_imports=pluralize(module.count_imports, 'import')))
    print('\n'.join(all_import))


def classes(module):
    all_class = {}
    for cls in module.get_classes():
        all_class[cls.name] = []

        for func in module.get_functions(cls.node):
            all_class[cls.name].append('\t\t-{name}'.format(name=func.name))

    print('This module contains {count} {word_class}:'.format(
        count=module.count_classes,
        word_class=pluralize(module.count_classes, 'class', 'classes')))

    for key, value in all_class.items():
        print('\t-{name}'.format(name=key))
        print('\n'.join(value))

    if module.count_classes == 0:
        print("This module {module} doesn't contains class.".format(
            module=module.path.name))


def summarize(analyze):
    stats = analyze.get_global_stats()
    print('This project contains {count} {word_class}'.format(
        count=stats['modules'],
        word_class=pluralize(stats['modules'], 'module')))
    print('This project contains {count} {word_class}'.format(
        count=stats['imports'],
        word_class=pluralize(stats['imports'], 'import')))
    print('This project contains {count} {word_class}'.format(
        count=stats['modules'],
        word_class=pluralize(stats['classes'], 'class', 'classes')))
