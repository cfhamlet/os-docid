import os
import sys
import argparse
from os_docid import docid


def check_exist(value):
    if not value:
        return value
    if not os.path.isfile(value):
        raise argparse.ArgumentTypeError('must an exist file')
    return value


def execute(argv=None):
    argv = argv or sys.argv
    parser = argparse.ArgumentParser(description='Generate DocID.')
    parser.add_argument(
        '-f', '--file', help='file to be process (default: stdin)',
        type=check_exist, action='store', dest='input_file')
    args = parser.parse_args(argv[1:])
    input_file = sys.stdin
    if args.input_file:
        input_file = open(args.input_file, 'r')
    for line in input_file:
        line = line.strip()
        d = None
        try:
            d = docid(line)
        except:
            pass
        print '\t'.join([i for i in (line, str(d))])


if __name__ == '__main__':
    execute()
