import puzzle10
from io import StringIO


def char_to_bits(char: str) -> str:
    if len(char) != 1:
        raise Exception('Given char must be excalty one!')
    byte = int(char, 16).to_bytes(1, 'big')
    # Source: https://stackoverflow.com/a/41436816/3949509
    return ''.join('{0:04b}'.format(byte[0]))


def string_to_bits(string: str) -> str:
    out = StringIO()
    for char in string:
        out.write(char_to_bits(char))
    value = out.getvalue()
    out.close()
    return value


def solve_part_1(hash_prefix):
    free = 0
    for hash_suffix in range(128):
        hash_str = '%s-%s' % (hash_prefix, hash_suffix)
        knot_hash = puzzle10.solve_part_2(hash_str)
        bits = string_to_bits(knot_hash)
        if len(bits) != 128:
            raise Exception('Unexpected lenght! (%d)' % len(bits))
        for bit in filter(lambda bit: bit == '1', bits):
            free += 1
    return free


def solve_part_2(puzzle_input):
    pass
