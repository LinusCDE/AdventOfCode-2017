#!/usr/bin/env python3

'''
Solve the Puzzles provided AdventOfCode.com year 2017!
'''

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from os.path import exists
from sys import argv
from sys import stderr
from time import time


verbose = False  # Whether the log-function will work. Is set by an argument.


def current_millis():
    '''Get milliseconds since 2017/01/01. Uses to determine execution time'''
    return int(time() * 1000)


def log(message):
    '''If verbose is active the message will get printed.
    This function gets injected into every puzzle<Day>-Module automatically.'''
    if verbose:
        print(message)


if __name__ == '__main__':  # Main part
    # Read arguments
    ap = ArgumentParser(description=__doc__,
                        formatter_class=RawDescriptionHelpFormatter)

    ap.add_argument('day', type=int, help='Which day/advent/puzzle to solve.')
    ap.add_argument('part', type=int, help='Which Part to solve (1 or 2).')
    ap.add_argument('--file', '-f', type=str, metavar='InputFile',
                    default=None, help='Custom input file for the puzzle')
    ap.add_argument('--input', '-i', type=str, metavar='InputString',
                    default=None, help='Custom input for the puzzle')
    ap.add_argument('--verbose', '-v', action='store_true',
                    default=False, help='Enable verbose logging')

    args = ap.parse_args()

    # Save verbose value globally
    verbose = args.verbose

    # Validate argument 'day' (only 1 to 24):
    if args.day < 1 or args.day > 24:
        print(argv[0], 'error', 'argument day', 'Only values between 1 and 24'
              + ' are allowed.', sep=': ', file=stderr)
        exit(1)

    # Validate argument 'part' (only 1 and 2):
    if args.part not in (1, 2):
        print(argv[0], 'error', 'argument part', 'Only the values 1 and 2 are'
              + ' allowed.', sep=': ', file=stderr)
        exit(1)

    # Name of module, function and input file for current puzzle
    module_name = 'puzzle' + str(args.day)
    func_name = 'solve_part_' + str(args.part)
    input_file_name = args.file if args.file else 'inputs/input%s' % args.day

    # Getting function for requested day and part:
    puzzle = None
    try:
        puzzle = __import__(name=module_name)
        if not hasattr(puzzle, func_name):
            raise Exception('Part not supported yet!')
        puzzle.log = log  # Injects log-function
    except Exception:
        print(argv[0], 'error', 'Day ' + str(args.day) + ', Part '
              + str(args.part) + ' can\'t be solved, yet.', sep=': ',
              file=stderr)
        exit(1)

    print('Solving Puzzle for Day ' + str(args.day)
          + ', Part ' + str(args.part) + '...')

    # Getting puzzle input:
    if not args.input:
        if not exists(input_file_name):
            print(argv[0], 'error', 'Day ' + str(args.day) + '.'
                  + 'Could not find the file \'%s\'!' % input_file_name,
                  sep=': ', file=stderr)
            exit(1)

        puzzle_input = None
        with open(input_file_name, 'r') as f:
            puzzle_input = f.read().strip()
    else:
        puzzle_input = args.input

    # Solving and measuring time:
    print(']--------------------------------------------------[')
    start_time = current_millis()
    solution = getattr(puzzle, func_name)(puzzle_input)
    end_time = current_millis()
    diff_millis = end_time - start_time

    # Printing solution and time:
    print('Solution:', solution)
    print('Duration:', (diff_millis // 1000), 'Seconds and',
          (diff_millis % 1000), 'Milliseconds')
    exit(0)
