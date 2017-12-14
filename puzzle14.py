from coordinate_utils import CoordinateField
from io import StringIO
from puzzle10 import solve_part_2 as gen_knot_hash


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
        knot_hash = gen_knot_hash(hash_str)
        bits = string_to_bits(knot_hash)
        if len(bits) != 128:
            raise Exception('Unexpected lenght! (%d)' % len(bits))
        for bit in filter(lambda bit: bit == '1', bits):
            free += 1
    return free


class Groupifier:

    def __init__(self, field: CoordinateField):
        self.field = field
        self.group_count = 0
        self.group_sizes = dict()  # Format: {id1: count1, ...}
        self.ids = CoordinateField(field.min_x, field.max_x,
                                   field.min_y, field.max_y)

    def index_group(self, new_index, x, y) -> int:
        if self.field[x, y] != 1 or self.ids.filled((x, y)):
            return 0
        self.ids[x, y] = new_index
        indexed = 1
        for adj_x, adj_y in self.field.adjectents((x, y), diagonals=False):
            indexed += self.index_group(new_index, adj_x, adj_y)
        return indexed

    def groupify(self):
        total = 0
        for x, y in self.field.coordinates(only_existing=False):
            indexed = self.index_group(self.group_count, x, y)
            total += indexed
            if indexed > 0:
                self.group_count += 1
                self.group_sizes[self.group_count-1] = indexed
        self.print_all_coords(10, 10)
        print(self.group_sizes)
        print(total)

    def print_all_coords(self, x_max, y_max):
        for x in range(x_max):
            for y in range(y_max):
                val = str(self.ids[x, y])
                while len(val) < 4:
                    val = ' ' + val
                print(val + '|', end='')
            print('')


def solve_part_2(hash_prefix):
    field = CoordinateField(0, 127, 0, 127)
    for hash_suffix_and_y in range(128):
        hash_str = '%s-%s' % (hash_prefix, hash_suffix_and_y)
        knot_hash = gen_knot_hash(hash_str)
        bits = string_to_bits(knot_hash)
        if len(bits) != 128:
            raise Exception('Unexpected lenght! (%d)' % len(bits))
        for x, bit in enumerate(bits):
            field[x][hash_suffix_and_y] = int(bit)

    groupifier = Groupifier(field)
    groupifier.groupify()
    return groupifier.group_count
