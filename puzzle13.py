class Layer:

    def __init__(self, depth: int, layer_range: int):
        self.depth, self.range = depth, layer_range
        self.position, self.direction = 0, 1

    def tick(self, steps: int=1):
        if steps == 0:
            return
        if self.direction == 1 and self.position == (self.range-1):
            self.direction = -1
        elif self.direction == -1 and self.position == 0:
            self.direction = 1

        self.position += self.direction
        if steps > 1:
            self.tick(steps - 1)


class Firewall:

    def __init__(self, puzzle_input: str):
        self.layers = {}  # Format: {depth: Layer(...)}
        self.max_depth = 0
        for line in puzzle_input.split('\n'):
            depth, layer_range = map(int, line.split(': '))
            self.layers[depth] = Layer(depth, layer_range)
            self.max_depth = max(self.max_depth, depth)

    def tick(self, steps: int=1):
        for layer in self.layers.values():
            layer.tick()

    def can_pass(self, depth: int) -> bool:
        if depth not in self.layers:
            return True

        return self.layers[depth].position != 0

    def reset(self):
        for layer in self.layers.values():
            layer.direction = 1
            layer.position = 0


def pass_through(firewall: Firewall):
    caught, serverity = False, 0
    for depth in range(firewall.max_depth + 1):
        if not firewall.can_pass(depth):
            caught = True
            serverity += (depth * firewall.layers[depth].range)
        firewall.tick()
    return caught, serverity


def solve_part_1(puzzle_input):
    return pass_through(Firewall(puzzle_input))[1]


def solve_part_2(puzzle_input):
    passed = False
    while not passed:
        
