from itertools import count


class Layer:

    def __init__(self, depth: int, layer_range: int):
        self.depth, self.range = depth, layer_range

    def position(self, ticks: int):
        '''
        Source: https://stackoverflow.com/a/11544567/3949509
        '''
        input_range = self.range - 1
        return abs(((ticks + input_range) % (input_range * 2)) - input_range)


class Firewall:

    def __init__(self, puzzle_input: str):
        self.ticks = 0
        self.layers = {}  # Format: {depth: Layer(...)}
        self.max_depth = 0
        for line in puzzle_input.split('\n'):
            depth, layer_range = map(int, line.split(': '))
            self.layers[depth] = Layer(depth, layer_range)
            self.max_depth = max(self.max_depth, depth)

    def tick(self, steps: int=1):
        self.ticks += steps

    def can_pass(self, depth: int) -> bool:
        if depth not in self.layers:
            return True

        return self.layers[depth].position(self.ticks) != 0

    def reset(self):
        for layer in self.layers.values():
            layer.direction = 1
            layer.position = 0

    def positions(self):
        pos = {}
        for layer in self.layers.values():
            pos[layer.depth] = layer.position
        return pos


def load(puzzle_input):
    max_depth = 0
    layers = {}  # Format: {depth: {pos: int, dir: int, range: int}, ...}
    for line in puzzle_input.split('\n'):
        depth, layer_range = map(int, line.split(': '))
        layers[depth] = {'pos': 0, 'dir': 1, 'range': layer_range}
        max_depth = max(max_depth, depth)
    return max_depth, layers


def solve_part_1(puzzle_input):
    firewall = Firewall(puzzle_input)
    serverity = 0
    for depth in range(firewall.max_depth + 1):
        if not firewall.can_pass(depth):
            serverity += (depth * firewall.layers[depth].range)
        firewall.tick()
    return serverity


def caught_and_reset(firewall: Firewall) -> int:
    for depth in range(firewall.max_depth + 1):
        if not firewall.can_pass(depth):
            return True
        firewall.tick()
    return False


def solve_part_2(puzzle_input):
    firewall = Firewall(puzzle_input)
    for ticks_delayed in count():
        firewall.ticks = ticks_delayed
        if not caught_and_reset(firewall):
            return ticks_delayed
