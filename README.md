# kojak ![](statics/logo-64x64.png) 

[![Build Status](https://travis-ci.org/4383/kojak.svg?branch=master)](https://travis-ci.org/4383/kojak)
![PyPI](https://img.shields.io/pypi/v/kojak.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/kojak.svg)
![PyPI - Status](https://img.shields.io/pypi/status/kojak.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Python projects analyzer

kojak is a development tools that help you to get informations
about a given python file and to get a big picture of this one
like all the module classes and all the module classes functions members.

kojak retrieve informations from python projects by using the python [abstract
tree syntax (AST)](https://docs.python.org/3/library/ast.html).

## Warning
Really young project with poor functionalities for now.

## Features
- Get classes and methods
- Get functions from python modules
- Get list of imports

## Install or Update kojak

```sh
$ pip install -U kojak
```

## Usage

```shell
$ # analyze a complete module
$ kojak ~/path/to/your/module/root/dir
$ # analyze a single python file
$ kojak ~/path/to/your/file.py
$ # analyze the current working dir
$ kojak
$ # analyze the current working dir alternative
$ kojak .
```

## Future improvements
- add the possibility to do a recursive of the whole files of a given project
- inspect from the stdin
- add the possibility to scoping an object or a given method or function

## Contribute

If you want to contribute to kojak [please first read the contribution guidelines](CONTRIBUTING.md)

## Licence

This project is under the MIT License.

[See the license file for more details](LICENSE)
