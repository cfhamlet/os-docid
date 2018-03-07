from __future__ import print_function

import argparse
import os
import sys

from os_docid import docid


def check_exist(value):
    if not value:
        return value
    if not os.path.isfile(value):
        raise argparse.ArgumentTypeError('must an exist file')
    return value


def print_all(line, d):
    print("\t".join((line, str(d))))


def print_docid(line, d):
    print(d)


OUTPUT = {'a': print_all, 'o': print_docid}


def execute(argv=None):
    argv = argv or sys.argv
    parser = argparse.ArgumentParser(description='Generate DocID.')
    parser.add_argument(
        '-f', '--file', help='file to be process (default: stdin)',
        type=check_exist, action='store', dest='input_file')
    parser.add_argument(
        '-o', '--output', help='output format (default: [o]nly docid)',
        default='o', action='store', dest='output', choices=OUTPUT.keys())
    args = parser.parse_args(argv[1:])

    input_file = sys.stdin
    if args.input_file:
        input_file = open(args.input_file, 'r')
    print_func = OUTPUT[args.output]

    for line in input_file:
        line = line.strip()
        if not line:
            continue
        d = None
        try:
            d = docid(line)
        except:
            pass
        print_func(line, d)


if __name__ == '__main__':
    execute()
