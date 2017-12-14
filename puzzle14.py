from coordinate_utils import CoordinateField
from puzzle10 import solve_part_2 as gen_knot_hash


def to_bits(string: str):
    '''Yields the bits for each char. Asuming the chars in the string are
    hexadecimal (0-F).'''
    for char in string:
        # Source for next line: https://stackoverflow.com/a/41436816/3949509
        byte = int(char, 16).to_bytes(1, 'big')
        yield ''.join('{0:04b}'.format(byte[0]))


def disk_bits(hash_prefix):
    '''Yields 128 bit strings for the disk using given 'hash_prefix'.'''
    for hash_suffix in range(128):
        # Generate knot-hash from day 10 part 2 and convert to bits:
        knot_hash = gen_knot_hash('%s-%s' % (hash_prefix, hash_suffix))
        bits = ''.join(to_bits(knot_hash))

        if len(bits) != 128:
            raise Exception('Unexpected length! (%d != 128)' % len(bits))
        yield bits


def solve_part_1(puzzle_input):
    free = 0
    for bits in disk_bits(puzzle_input):
        for _ in filter(lambda bit: bit != '0', bits):
            free += 1
    return free


def count_group(field: CoordinateField, pos: tuple) -> int:
    '''Finds a group recursivly and returns the amount of found
    coordinates.'''
    if field[pos] != 1:  # Skip grouped (= 'None') and 0s
        return 0

    del field[pos]  # Remove found/grouped numbers
    found = 1

    # Search for adjecent coordinates recursivly:
    for adjecent in field.adjectents(pos, diagonals=False):
        found += count_group(field, adjecent)
    return found


def groups(field):
    group_count = 0
    field = field.copy()  # Copy field, since grouped coordinates are removed

    # Search for groups:
    for pos in field.coordinates(only_existing=False):
        if count_group(field, pos) > 0:
            group_count += 1
    return group_count


def solve_part_2(puzzle_input):
    field = CoordinateField(0, 127, 0, 127)  # 128x128

    # Filling coordinate field with 1s and 0s:
    for y, bits in enumerate(disk_bits(puzzle_input)):
        for x, bit in enumerate(map(int, bits)):
            field[x, y] = bit

    return groups(field)
