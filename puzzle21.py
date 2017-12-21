from coordinate_utils import CoordinateField


class PixelGrid(CoordinateField):

    def empty_copy(self) -> 'PixelGrid':
        return PixelGrid(self.min_x, self.max_x, self.min_y, self.max_y)

    def __hash__(self):
        data = []
        for x, y, value in self.items():
            data.append(x)
            data.append(y)
            data.append(1 if value == '#' else 0)
        data.append(99)  # the 99 has no meaning
        # print('%s => %d' % (data, hash(tuple(data))))
        return hash(tuple(data))

    def __eq__(self, other):  # dict() also uses this to ensure a match
        return hash(self) == hash(other)


def flat_to_grid(flat) -> PixelGrid:
    rows = flat.split('/')
    max_x, max_y = len(rows[0]) - 1, len(rows) - 1
    grid = PixelGrid(0, max_x, 0, max_y)
    for y, row in enumerate(flat.split('/')):
        for x, char in enumerate(row):
            grid[x, y] = char
    return grid


def print_grid(grid: PixelGrid):
    for y in range(grid.max_y+1):
        for x in range(grid.max_x+1):
            print(grid[x, y], end='')
        print('')


def print_grid_grid(grid: PixelGrid):
    for y in range(grid.max_y+1):
        for x in range(grid.max_x+1):
            count = 0
            for value in grid.values():
                if value is not None:
                    count += 1
            print(count, end='')
        print('')


def rotated_90(grid: PixelGrid):
    '''Returns a copy of the grid that is rotated by 90 degrese.'''
    copy = grid.empty_copy()
    for x, y, value in grid.items():
        copy[grid.max_y - y, x] = value
    return copy


def flipped_horizontal(grid: CoordinateField):
    copy = grid.empty_copy()
    for x, y, value in grid.items():
        copy[grid.max_x - x, y] = value
    return copy


def load_rules(puzzle_input):
    rules = {}  # Format: {rule_in: rule_out}
    for line in puzzle_input.split('\n'):
        rule_in1, rule_out = map(flat_to_grid, line.split(' => '))
        rule_in2 = flipped_horizontal(rule_in1)
        rule_in3 = rotated_90(rule_in1)
        rule_in4 = flipped_horizontal(rotated_90(rule_in3))
        rules[rule_in1] = rule_out
        rules[rule_in2] = rule_out
        rules[rule_in3] = rule_out
        rules[rule_in4] = rule_out

        print_grid(rule_in1)
        print_grid(rule_in2)
        print_grid(rule_in3)
        print_grid(rule_in4)
    return rules


def to_grid_grid(master_grid: PixelGrid):
    inner_size = 3 if (master_grid.max_x+1) % 3 == 0 else 2
    outer_size = (master_grid.max_x+1) // inner_size

    grid_grid = PixelGrid(0, outer_size-1, 0, outer_size-1)

    for x, y in grid_grid.coordinates(only_existing=False):
        grid_grid[x, y] = PixelGrid(0, inner_size-1, 0, inner_size-1)

    for mgx, mgy, value in master_grid.items():
        grid_grid_x = mgx // outer_size
        grid_grid_y = mgy // outer_size

        child = grid_grid[grid_grid_x, grid_grid_y]

        inner_x = mgx % outer_size
        inner_y = mgy % outer_size

        child[inner_x, inner_y] = value

    return grid_grid


def to_master_grid(grid_grid: PixelGrid):
    outer_size = grid_grid.max_x + 1
    inner_size = grid_grid[0, 0].max_x + 1  # Suppose all grid are equal
    master_grid = PixelGrid(0, (outer_size * inner_size) - 1,
                            0, (outer_size * inner_size) - 1)

    for ggx, ggy, grid in grid_grid.items():
        for ix, iy, value in grid.items():
            master_grid[ggx * outer_size + ix, ggy * outer_size + iy] = value

    return master_grid


def sharpen(source_grid: PixelGrid, rules: dict) -> PixelGrid:
    if source_grid.max_x in (1, 2):
        return rules[source_grid]

    grid_grid = to_grid_grid(source_grid)
    for x, y, grid in grid_grid.items():
        print('Rule for:')
        print_grid(grid)
        grid_grid[x, y] = rules[grid]
    return to_master_grid(grid_grid)


def solve_part_1(puzzle_input):
    rules = load_rules(puzzle_input)
    print(len(rules))
    start = flat_to_grid('.#./..#/###')
    #r1 = rules[start]
    #rs = to_grid_grid(r1)
    #rm = to_master_grid(rs)
    #print_grid(rm)
    s1 = sharpen(start, rules)
    print_grid(s1)
    s2 = sharpen(s1, rules)
    print_grid(s2)


def solve_part_2(puzzle_input):
    pass
