from coordinate_utils import CoordinateField


# DISCLAIMER:
# This puzzle could perform significantly better if it wasn't such heavy
# with the use of OOP (classes). But it should be easier to understand.


print('Hint: Run this puzzle with \'pypy3\' to get vastly improved '
      'performance in part 2.')


class PixelGrid(CoordinateField):
    '''A hashable CoordinateField.'''

    def empty_copy(self) -> 'PixelGrid':
        '''Returns an empty copy of this PixelGrid, which has the same size.'''
        return PixelGrid(self.min_x, self.max_x, self.min_y, self.max_y)

    def __hash__(self) -> int:
        '''Returns a hash based on the data inside.
        This isn't very efficient and only expects small grids with
        single chars inside.

        Be aware that infinite grids will raise an Exception!

        Needed for the use in dict().
        '''
        data = []  # Will be converted to a tuple and hashed
        for x, y, value in self.items(only_existing=False):
            data.append(x)
            data.append(y)
            data.append(ord(value))
        data.append(99)  # the 99 has no meaning
        return hash(tuple(data))

    def __eq__(self, other: 'PixelGrid') -> bool:
        '''PixelGrids are equal when they have the same content (= hash).
        Needed for the use dict() as well.'''
        return hash(self) == hash(other)


def flat_to_grid(flat) -> PixelGrid:
    '''Converts rows seperated by a '/' into a PixelGrid and returns that.'''
    rows = flat.split('/')
    max_x, max_y = len(rows[0]) - 1, len(rows) - 1  # Sizes of the PixelGrid
    grid = PixelGrid(0, max_x, 0, max_y)

    for y, row in enumerate(flat.split('/')):
        for x, char in enumerate(row):
            grid[x, y] = char

    return grid


def print_grid(grid: PixelGrid):
    '''Prints the current grid.
    Isn't used any longer but remains for potential debugging purposes.
    '''
    for y in range(grid.max_y+1):
        for x in range(grid.max_x+1):
            print(grid[x, y], end='')
        print('')


def rotated_90(grid: PixelGrid):
    '''Returns a copy of the given 'grid' that is rotated by 90 degrese.'''
    copy = grid.empty_copy()

    for x, y, value in grid.items():
        copy[grid.max_y - y, x] = value  # Notice the swapped x- and y-axes

    return copy


def flipped_horizontal(grid: CoordinateField):
    '''Returns a copy of given 'grid' that is flipped horizontally.'''
    copy = grid.empty_copy()

    for x, y, value in grid.items():
        copy[grid.max_x - x, y] = value  # x-axis iterated backwards

    return copy


def load_rules(puzzle_input) -> dict:
    '''Generates all possible rules from the 'puzzle_input' and returns
    them as a dict.
    '''
    rules = {}  # Format: {rules_in: rules_out} (containing PixelGrids)

    for line in puzzle_input.split('\n'):
        # Load and generate 7 possible input fields:
        rule_in1, rule_out = map(flat_to_grid, line.split(' => '))
        rule_in2 = flipped_horizontal(rule_in1)
        rule_in3 = rotated_90(rule_in1)
        rule_in4 = flipped_horizontal(rotated_90(rule_in3))
        rule_in5 = rotated_90(rule_in3)
        rule_in6 = rotated_90(rule_in5)
        rule_in7 = flipped_horizontal(rule_in6)

        # Add all 7 rules to the set. They are more or less random
        # but they work and seem needed:
        rules[rule_in1] = rules[rule_in2] = rules[rule_in3] = rule_out
        rules[rule_in4] = rules[rule_in5] = rules[rule_in6] = rule_out
        rules[rule_in7] = rule_out

    return rules


def to_grid_grid(master_grid: PixelGrid):
    '''Returns a smaller grid which contains all 2x2 or 3x3 chunks as
    the values using 'master_grid'. ( grids in grids = grid_grid ;) ).
    '''

    # ----- Setup: -----
    # The size the child grids should have:
    inner_size = 2 if ((master_grid.max_x + 1) % 2 == 0) else 3

    # The size of the result when inner_size is compressed to a size of 1x1:
    outer_size = (master_grid.max_x + 1) // inner_size

    grid_grid = PixelGrid(0, outer_size - 1, 0, outer_size - 1)  # Result grid

    # Fill grid_grid with empty child grids:
    for x, y in grid_grid.coordinates(only_existing=False):
        grid_grid[x, y] = PixelGrid(0, inner_size-1, 0, inner_size-1)

    # ----- Filling (compression): ------
    # Get all values from 'master_grid' and put them into the 'grid_grid'
    # at the appropriate places.                       ↓↓↓↓↓- child grid
    # Example: master_grid[0, 1] ==(>) grid_grid[0, 0][0, 1]
    for master_x, master_y, value in master_grid.items():

        # The child_grid position for the current coordinate:
        child_grid_x = master_x // inner_size
        child_grid_y = master_y // inner_size

        child = grid_grid[child_grid_x, child_grid_y]

        # Position in the child grid: ( = the remainder of child_grid_* )
        inner_x = master_x % inner_size
        inner_y = master_y % inner_size

        child[inner_x, inner_y] = value

    return grid_grid


def to_master_grid(grid_grid: PixelGrid):
    '''Returns a big "master grid" containing all child grids in 'grid_grid'
    completly. ( = reversion of to_grid_grid(...) )
    '''

    # ----- Setup: -----
    outer_size = grid_grid.max_x + 1
    inner_size = grid_grid[0, 0].max_x + 1  # Suppose all grid are equal
    master_grid = PixelGrid(0, (outer_size * inner_size) - 1,
                            0, (outer_size * inner_size) - 1)

    # --- Filling (decompression): -----
    for grid_grid_x, grid_grid_y, child in grid_grid.items():
        for inner_x, inner_y, value in child.items():

            master_grid[grid_grid_x * inner_size + inner_x,
                        grid_grid_y * inner_size + inner_y] = value

    return master_grid


def sharpened(grid: PixelGrid, rules: dict, generations: int) -> PixelGrid:
    '''Returns a sharpned version of the given 'grid' using 'rules'.'''

    for current_generation in range(1, generations+1):
        print('Generation %d/%d...' % (current_generation, generations))

        if grid.max_x in (1, 2):  # = either 2x2 or 3x3 (max_x == size -1)
            grid = rules[grid]
            continue  # Don't need to split a simple grid

        # Split grid into multiple small grids in a grid: (yes, it's confusing)
        grid_grid = to_grid_grid(grid)

        # Apply rules for each child PixelGrids in the grid_grid:
        for x, y, grid in grid_grid.items():
            grid_grid[x, y] = rules[grid]

        # Unify PixelGrid again to one big grid:
        grid = to_master_grid(grid_grid)

    return grid


def count_lights(grid: PixelGrid) -> int:
    '''Returns the amound of all the lights/#'s in the given 'grid'.'''
    count = 0

    for value in grid.values():
        if value == '#':
            count += 1

    return count


def solve_part_1(puzzle_input):
    rules = load_rules(puzzle_input)

    start_grid = flat_to_grid('.#./..#/###')  # <- As defined by the puzzle
    return count_lights(sharpened(start_grid, rules, generations=5))


def solve_part_2(puzzle_input):
    rules = load_rules(puzzle_input)

    start_grid = flat_to_grid('.#./..#/###')  # <- As defined by the puzzle
    return count_lights(sharpened(start_grid, rules, generations=18))
