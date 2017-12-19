from coordinate_utils import CoordinateField, add, direction


# Argument for aoc.py. When set to False the puzzle_input doesn't
# get stripped, which would destroy some coordinates:
AOC_STRIP_INPUT = False


def load_route(puzzle_input) -> CoordinateField:
    '''Puts the content of 'puzzle_input' into a CordinateField
    and returns it.
    '''
    field = CoordinateField()
    highest_x, highest_y = 0, 0

    for y, line in enumerate(puzzle_input.split('\n')):
        highest_y = y
        for x, char in enumerate(line):
            highest_x = max(highest_x, x)
            field[x, y] = char

    field.set_size(0, highest_x, 0, highest_y)
    return field


def is_letter(char: str):
    '''Returns whether the character ('char') is one of the searched letters.'''
    if not isinstance(char, str):
        return False
    return char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def is_road(char: str):
    '''Returns whether this character ('char') is part of a road.
    A road can be '|', '-' or any uppercase letter (see 'is_letter(char)').'''
    return char in ('|', '-') or is_letter(char)


def follow(field: CoordinateField, pos):
    '''Finds and yields all positions and their values,
    following 'pos' downwards.
    '''
    last_pos = add(pos, (0, -1))  # Inital direction is: down

    while True:  # Will be left manually
        char = field[pos]  # Char at curren position
        yield pos[0], pos[1], char

        if is_road(char):  # Move forward the same direction
            next_pos = add(pos, direction(last_pos, pos))

            # Finish if out of coordinate field or nothing (space) found:
            if not field.in_field(next_pos) or \
               (not is_road(field[next_pos]) and field[next_pos] != '+'):
                return  # Finished
        else:
            if char != '+':
                raise Exception('Unexpected character: %s' % char)

            # Encountered a '+'. Need to choose new direction:
            for possible in field.adjectents(pos, diagonals=False):
                nchar = field[possible]
                if possible != last_pos and is_road(nchar):
                    next_pos = possible
                    break
            else:
                raise Exception('No direction found in which to turn.')

        last_pos, pos = pos, next_pos


def find_entry_position(field: CoordinateField) -> tuple:
    '''Determines and returns entry point of the coordinate field.'''
    for x, y, value in field.items():
        if is_road(value) and y == 0:
            return x, y
    else:
        raise Exception('No entry position found!')


def solve_part_1(puzzle_input):
    field = load_route(puzzle_input)

    entry_pos, letters = find_entry_position(field), []

    for x, y, char in follow(field, entry_pos):
        if is_letter(char):
            letters.append(char)

    return ''.join(letters)


def solve_part_2(puzzle_input):
    field = load_route(puzzle_input)

    entry_pos, count = find_entry_position(field), 0

    for _ in follow(field, entry_pos):
        count += 1

    return count
