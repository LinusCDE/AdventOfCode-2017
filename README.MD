# Solving Puzzles at [AdventOfCode.com](https://adventofcode.com/2017)

## General
In this repo I'll solve the AoC-Challanges as far as I want (and have time) to.

Feel Free to use this as a simplified structure for your own scripts.

## Installation

- Install python3
- `$ pip3 install argparse`
- Download this repo
- Go into the directory of this repo
- `$ python aoc.py -h`


## Structure

Your solutions go into the same directory as the main file `aoc.py` named `puzzle<Day>.py`

### Example content `puzzle<Day>.py`
```python3
def solve_part_1(puzzle_input):
    return "My solution for part 1"

def solve_part_2(puzzle_input):
    return "My solution for part 2"
```

### Tipp
You can use the `log(message)`-Function as defined in `aoc.py`. It'll be automatically injected upon execution time.

### Input/Puzzle

You can either specify a file using `--file <Path>`, a string for short inputs with `--input <Input>` or place the file into `inputs/input<Day>` (without any file extension).

## Disclaimer

The inputs found, are my personal ones. If you want your solution, you can replace them with your own or specify with `--path` or `--input`.
