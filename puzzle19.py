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
        return (VEC_DOWN, VEC_UP)
    elif char == '-':
        return (VEC_LEFT, VEC_RIGHT)


def is_road(char):
    return char in ('|', '-')


def is_letter(char):
    if not isinstance(char, str):
        return False
    return char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def find_next(field: CoordinateField, pos, last_pos):
    char = field[pos]
    dirs = directions(char)
    #print(dirs)
    if dirs is not None or is_letter(char):
        #print('Vec')
        vector = pos[0] - last_pos[0], pos[1] - last_pos[1]
        return pos[0] + vector[0], pos[1] + vector[1]
    if char == '+':
        print('TURN')
        for possible in field.adjectents(pos, diagonals=False):
            nchar = field[possible]
            if possible != last_pos \
             and (directions(nchar) is not None or is_letter(nchar)):
                return possible
    raise Exception('No further position found! (%d, %d: %s)'
                    % (pos[0], pos[1], field[pos]))


def find_entry_point(field: CoordinateField):
    for x, y, value in field.items():
        print(x, y, '%s' % value)
        if value is not None and value != ' ' and y == 0:
            return x, y
    else:
        raise Exception('No Entry found!')


def solve_part_1(puzzle_input):
    with open('/tmp/input.txt') as file:
        puzzle_input = file.read()
    field = load_route(puzzle_input)
    values = []
    pos = None

    pos = find_entry_point(field)
    last_pos = pos[0], pos[1] - 1
    c = 0
    while True:
        c += 1
        try:
            next_pos = find_next(field, pos, last_pos)
            print(next_pos)
            if field[next_pos] is None or field[next_pos] == ' ':
                print(next_pos)
                print('Part 2: %d' % c)
                return ''.join(values)

            if is_letter(field[next_pos]):
                values.append(field[next_pos])
            last_pos, pos = pos, next_pos
        except Exception as e:  # Coordinate fail (outside of bounds)
            print(e.message)
            print('Part 2: %d' % c)
            return ''.join(values)


def solve_part_2(puzzle_input):
    pass
