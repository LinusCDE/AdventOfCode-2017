from io import StringIO
from puzzle3 import get_value, put_value
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


NEIGHBOURS = (
    (0, -1),  # Top
    (-1, 0),  # Left
    (1, 0),  # Right
    (0, 1),  # Bottom
)


def get_adjecents(pos: list, x_size=128, y_size=128):
    for neigbour in NEIGHBOURS:
        adjecent = (pos[0] + neigbour[0], pos[1] + neigbour[1])
        if min(adjecent) < 0:
            continue
        if adjecent[0] >= x_size or adjecent[1] >= y_size:
            continue
        yield adjecent


class Groupifier:

    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.group_count = 0
        self.group_sizes = dict()  # Format: {id1: count1, ...}
        self.group_ids = dict()  # Infinite Matrix

    def index_group(self, new_index, x, y) -> int:
        if self.coordinates[x][y] != 1 \
         or get_value(self.group_ids, (x, y)) is not None:
            return 0
        put_value(self.group_ids, (x, y), new_index)
        indexed = 1
        for adj_x, adj_y in get_adjecents((x, y)):
            indexed += self.index_group(new_index, adj_x, adj_y)
        return indexed

    def groupify(self):
        total = 0
        for x in range(len(self.coordinates)):
            for y in range(len(self.coordinates[x])):
                indexed = self.index_group(self.group_count, x, y)
                total += indexed
                if indexed > 0:
                    self.group_count += 1
                    self.group_sizes[self.group_count-1] = indexed
        self.print_all_coords(6, 6)
        print(self.group_sizes)
        print(total)

    def print_coords(self, pos, radius=10):
        for xoffset in range(-radius, radius+1):
            for yoffset in range(-radius, radius+1):
                x = pos[0] + xoffset
                y = pos[1] + yoffset
                val = str(get_value(self.group_ids, (x, y)))
                while len(val) < 4:
                    val = ' ' + val
                suffix = '<' if pos == (x, y) else '|'
                print(val + suffix, end='')
            print('')

    def print_all_coords(self, x_max, y_max):
        for x in range(x_max):
            for y in range(y_max):
                val = str(get_value(self.group_ids, (x, y)))
                while len(val) < 4:
                    val = ' ' + val
                print(val + '|', end='')
            print('')


def solve_part_2(hash_prefix):
    coordinates = [[0] * 128] * 128
    for hash_suffix_and_y in range(128):
        hash_str = '%s-%s' % (hash_prefix, hash_suffix_and_y)
        knot_hash = gen_knot_hash(hash_str)
        bits = string_to_bits(knot_hash)
        if len(bits) != 128:
            raise Exception('Unexpected lenght! (%d)' % len(bits))
        for x, bit in enumerate(bits):
            coordinates[x][hash_suffix_and_y] = int(bit)

    xcoordinates = [
        [0, 1, 1, 0, 1, 1],
        [0, 1, 1, 0, 0, 1],
        [0, 0, 0, 1, 1, 1],
        [1, 1, 1, 1, 1, 0],
        [1, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 1, 0]
    ]
    groupifier = Groupifier(coordinates)
    groupifier.groupify()
    return groupifier.group_count
