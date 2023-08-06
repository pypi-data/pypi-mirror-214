# vomit

[![Tests](https://github.com/bhmt/vomit/actions/workflows/tests.yml/badge.svg)](https://github.com/bhmt/vomit/actions/workflows/tests.yml)

Make your python code somewhat unintelligible but still readable and still **functional**.

Change the utf8 encoding of class names, function names, function args, and name nodes with a fitting unicode representation.
Or switch those back from unicode to utf8.

The ast is used and does not keep formating.

The changes are inplace if using a file or a directory for input.

## Installation

the package is available on pypi and can be installed using pip.
Activate a virtual environment and run

```

pip install py-vomit

```

## Usage

As a module run vomit with either encode or decode required option.
For input use a a stdin + stdout, a file, or a directory.


```shell

usage: python -m vomit [-h] (-e | -d) [-f FILE | -s SOURCE]

options:
  -h, --help            show this help message and exit
  -e, --encode          indicate the file should be encoded
  -d, --decode          indicate the file should be decoded
  -f FILE, --file FILE  the file to encode or decode, defaults to stdin
  -s SOURCE, --source SOURCE
                        the directory to encode or decode .py files recursively

```


or use vomit as a library

```py

from vomit import to_unicode
from vomit import to_utf8
from vomit import UNICODE_MAP

print(to_utf8('a'))
# 'a'
print(to_unicode('a'))
# '𝔞'
print(UNICODE_MAP['0'])
# 0０𝟎𝟘𝟢𝟬𝟶🯰

```