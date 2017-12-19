from coordinate_utils import CoordinateField
from puzzle3 import VEC_UP, VEC_RIGHT, VEC_DOWN, VEC_LEFT


def load_route(puzzle_input) -> CoordinateField:
    field = CoordinateField()
    highest_x, highest_y = 0, 0
    for y, line in enumerate(puzzle_input.split('\n')):
        highest_y = y
        for x, char in enumerate(line):
            highest_x = max(highest_x, x)
            field[x, y] = char

    field._infinite = False
    field._min_x, field._min_y = 0, 0
    field._max_x, field._max_y = highest_x, highest_y
    return field


def directions(char):
    if char == '|':
        possible_dirs = (VEC_DOWN, VEC_UP)
    elif char == '-':
        possible_dirs = (VEC_LEFT, VEC_RIGHT)


def is_road(char):
    return char in ('|', '-')


def next_pos(field, pos, last_positions=list()):
    if len(last_positions) > 10:
        last_positions.pop()
    possible_dirs = []
    char = field[pos]
    if char is None:
        raise Exception('Impossible position! (%d, %d)' % pos)
    if is_road(char):  # On Road
        possible_dirs = directions(char)
        last_char = field[last_positions[0]]



def solve_part_1(puzzle_input):
    field = load_route(puzzle_input)
    values = []
    for value in filter(lambda v: v is not None, field.values()):
        if value not in ('-', '|', '+', ' '):
            values.append(value)

    from itertools import permutations
    for perm in permutations(values):
        print(''.join(perm))
    #return drive(field, (0, 0))


def solve_part_2(puzzle_input):
    pass
