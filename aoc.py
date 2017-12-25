#!/usr/bin/env python3

'''
Solve the Puzzles provided AdventOfCode.com year 2017!
'''

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
import gc
from os.path import exists
from sys import argv
from sys import stderr
from time import time


verbose = False  # Whether the log-function will work. Is set by an argument.


def time_str(millis, precision=3):
    '''Converts millisconds to a string that is nice to read'''
    # A higher precision than 3 digits is not useful.
    # To see this yourself just execute 'time.time(), time.time()' multiple
    # times and see the fluctuation yourself
    string = ('%.' + str(precision) + 'f milliseconds') % (millis % 1000)
    if millis >= 1000:  # At least one second
        seconds = int(millis) // 1000
        # Only write 'seconds' for one seconds. Respecting grammar. ;)
        template = '%d second and %s' if seconds is 1 else '%d seconds and %s'
        string = template % (seconds, string)
    return string


def log(message):
    '''If verbose is active the message will get printed.
    This function gets injected into every puzzle<Day>-Module automatically.'''
    if verbose:
        print(message, file=stderr)


if __name__ == '__main__':  # Main part
    # Read arguments
    ap = ArgumentParser(description=__doc__,
                        formatter_class=RawDescriptionHelpFormatter)

    ap.add_argument('day', type=int, help='Which day/advent/puzzle to solve.')
    ap.add_argument('part', type=int, help='Which Part to solve (1 or 2).')
    ap.add_argument('--file', '-f', type=str, metavar='InputFile',
                    default=None, help='Custom input file for the puzzle.')
    ap.add_argument('--input', '-i', type=str, metavar='InputString',
                    default=None, help='Custom input for the puzzle.')
    ap.add_argument('--verbose', '-v', action='store_true',
                    default=False, help='Enable verbose logging. Does not'
                    ' work with "--repeat".')
    ap.add_argument('--repeat', '-n', type=int, metavar='times',
                    default=1, help='Repeat multiple times for a best time.')
    ap.add_argument('--no-garbage-collect', '-G', action='store_true',
                    default=False, help='Disable automatic garbage collection'
                    ' during solving. Impacts timings and should be tried both'
                    ' since there does not seem to be good rule for when it is'
                    ' useful.')

    args = ap.parse_args()

    # Validate argument 'day' (only 1 to 25):
    if args.day < 1 or args.day > 25:
        print(argv[0], 'error', 'argument day', 'Only values between 1 and 25'
              + ' are allowed.', sep=': ', file=stderr)
        exit(1)

    # Validate argument 'part' (only 1 and 2):
    if args.part not in (1, 2):
        print(argv[0], 'error', 'argument part', 'Only the values 1 and 2 are'
              + ' allowed.', sep=': ', file=stderr)
        exit(1)

    # Validate argument 'repeat' (only a positive number):
    if args.repeat < 1:
        print(argv[0], 'error', 'argument number', 'Only positive numbers'
              + ' are allowed.', sep=': ', file=stderr)
        exit(1)

    # Save verbose value globally
    verbose = args.verbose and args.repeat is 1
    if args.verbose and args.repeat > 1:
        print('Warn: Disabled verbose logging because of --repeat is higher'
              + ' than 1 (see --help)', file=stderr)

    # Name of module, function and input file for current puzzle
    module_name = 'puzzle' + str(args.day)
    func_name = 'solve_part_' + str(args.part)
    input_file_name = args.file if args.file else 'inputs/input%s' % args.day

    # Getting function for requested day and part:
    puzzle, strip_input = None, True
    try:
        puzzle = __import__(name=module_name)
        if not hasattr(puzzle, func_name):
            raise Exception('Part not supported yet!')
        puzzle.log = log  # Injects log-function
        if hasattr(puzzle, 'AOC_STRIP_INPUT'):
            strip_input = puzzle.AOC_STRIP_INPUT
    except Exception:
        print(argv[0], 'error', 'Day ' + str(args.day) + ', Part '
              + str(args.part) + ' can\'t be solved, yet.', sep=': ',
              file=stderr)
        exit(1)

    print('Solving Puzzle for Day ' + str(args.day)
          + ', Part ' + str(args.part) + '...', file=stderr)

    # Getting puzzle input:
    if not args.input:
        if not exists(input_file_name):
            print(argv[0], 'error', 'Day ' + str(args.day) + '.'
                  + 'Could not find the file \'%s\'!' % input_file_name,
                  sep=': ', file=stderr)
            exit(1)

        puzzle_input = None
        with open(input_file_name, 'r') as f:
            puzzle_input = f.read()
            if strip_input:
                puzzle_input = puzzle_input.strip()
    else:
        puzzle_input = args.input

    # Solving and measuring time:
    if verbose:
        print(']---------------------------------------------[', file=stderr)
    solve_it = getattr(puzzle, func_name)  # Func that solves the target puzzle
    timings = []  # Execution times in milliseconds

    # Disable garbage collection is requested:
    if args.no_garbage_collect:
        gc.disable()

    # Execute solve_it for the given amount (see '--repeat')
    for _ in range(args.repeat):
        if args.no_garbage_collect:
            gc.collect()  # Manual garbage collection between timings
        start, solution, end = time(), solve_it(puzzle_input), time()
        timings.append((end * 1000) - (start * 1000))

    # Reenable garbage collection if disabled:
    if not gc.isenabled():
        gc.enable()

    # Print solution and time:
    print('Solution:\t', solution)
    if(len(timings) is 1):
        print('Time:\t\t', time_str(timings[0]))
    else:
        print('Best time:\t', time_str(min(timings)))
        print('Avagerage time:\t', time_str(sum(timings) / len(timings)))
        print('Worst time:\t', time_str(max(timings)))
    exit(0)
