#!/usr/bin/env python

import argparse
import sys

from . import __version__
from .x import docid

_PY3 = sys.version_info[0] == 3
if _PY3:
    binary_stdin = sys.stdin.buffer
    binary_stdout = sys.stdout.buffer
else:
    binary_stdin = sys.stdin
    binary_stdout = sys.stdout


def execute(argv=None):
    argv = argv or sys.argv

    parser = argparse.ArgumentParser(description='Generate DocID.')

    parser.add_argument('-v', '--version',
                        action='version',
                        version='%(prog)s {version}'.format(
                                version=__version__)
                        )

    parser.add_argument('-f', '--file',
                        help='file to be process (default: stdin)',
                        nargs='+',
                        type=argparse.FileType('rb'),
                        default=[binary_stdin],
                        dest='input')

    args = parser.parse_args(argv[1:])

    for line in args.input[0]:
        line = line.strip()
        if not line:
            continue
        d = b'E'
        try:
            d = str(docid(line)).encode()
        except:
            pass
        binary_stdout.write(d)
        binary_stdout.write(b'\t')
        binary_stdout.write(line)
        binary_stdout.write(b'\n')


if __name__ == '__main__':
    execute()
