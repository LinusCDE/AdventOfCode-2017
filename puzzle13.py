from itertools import count

print('Hint: Run this puzzle with \'pypy3\' to get improved performance '
      'in part 2')


class Firewall:
    '''Representation of the firewall in the puzzle.'''

    def __init__(self, puzzle_input: str):
        self.ticks = 0  # Current picoseconds
        self.range_by_depth = dict()  # Format: {depth: range}
        self.max_depth = 0

        # Fill 'self.max_depth' and 'self.range_by_depth':
        for line in puzzle_input.split('\n'):
            depth, layer_range = map(int, line.split(': '))
            self.range_by_depth[depth] = layer_range
            self.max_depth = max(self.max_depth, depth)

    def tick(self):
        '''Increments one tick.'''
        self.ticks += 1

    def layer_position(self, depth) -> int:
        '''Returns the current layer position.
        If no layer exists, -1 will be returned.
        '''
        if depth not in self.range_by_depth:
            return -1

        # Source: https://stackoverflow.com/a/11544567/3949509
        layer_range = self.range_by_depth[depth] - 1
        return abs(((self.ticks + layer_range) % (layer_range * 2)) - layer_range)


def solve_part_1(puzzle_input):
    firewall = Firewall(puzzle_input)
    serverity = 0
    for depth in range(firewall.max_depth + 1):
        if firewall.layer_position(depth) == 0:
            serverity += (depth * firewall.range_by_depth[depth])
        firewall.tick()
    return serverity


def caught(firewall: Firewall) -> bool:
    '''Returns whether you would get caught in the 'firewall'.'''
    for depth in range(firewall.max_depth + 1):
        if firewall.layer_position(depth) == 0:
            return True
        firewall.tick()
    return False


def solve_part_2(puzzle_input):
    firewall = Firewall(puzzle_input)
    for ticks_delayed in count():
        # Try with different delays:
        firewall.ticks = ticks_delayed
        if not caught(firewall):
            return ticks_delayed
