#!/usr/bin/env python
from __future__ import print_function

import argparse
import os
import sys

from os_docid import docid

PY3 = sys.version_info[0] == 3


def check_exist(value):
    if not value:
        return value
    if not os.path.isfile(value):
        raise argparse.ArgumentTypeError('must an exist file')
    return value


def _get_input(args):
    io_input = sys.stdin
    if PY3:
        io_input = sys.stdin.buffer

    if args.input_file:
        io_input = open(args.input_file, 'rb')

    return io_input


def _get_output(args):
    io_output = sys.stdout
    if PY3:
        io_output = sys.stdout.buffer
    return io_output


def output_all(io_output, line, d):
    io_output.write(line)
    io_output.write(b'\t')
    if d is None:
        io_output.write(b'None')
    else:
        io_output.write(d.bytes())
    io_output.write(b'\n')


def output_docid(io_output, line, d):
    if d is None:
        io_output.write(b'None')
    else:
        io_output.write(d.bytes())
    io_output.write(b'\n')


OUTPUT = {'a': output_all, 'o': output_docid}


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

    io_input = _get_input(args)
    io_output = _get_output(args)
    output_func = OUTPUT[args.output]

    for line in io_input:
        line = line.strip()
        if not line:
            continue
        d = None
        try:
            d = docid(line.decode('ascii'))
        except:
            pass
        output_func(io_output, line, d)


if __name__ == '__main__':
    execute()
