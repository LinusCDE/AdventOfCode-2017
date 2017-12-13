from itertools import count


class Layer:

    def __init__(self, depth: int, layer_range: int):
        self.depth, self.range = depth, layer_range
        self.position, self.direction = 0, 1

    def tick(self, steps=1, backwards=False):
        if steps == 0:
            return
        direction = self.direction * -1 if backwards else self.direction
        if direction == 1 and self.position == (self.range-1):
            direction = -1
            self.direction *= -1
        elif direction == -1 and self.position == 0:
            direction = 1
            self.direction *= -1

        self.position += direction
        if steps > 1:
            self.tick(steps - 1, backwards=backwards)


class Firewall:

    def __init__(self, puzzle_input: str):
        self.tick_checkpoint = 0
        self.ticks = 0
        self.layers = {}  # Format: {depth: Layer(...)}
        self.max_depth = 0
        for line in puzzle_input.split('\n'):
            depth, layer_range = map(int, line.split(': '))
            self.layers[depth] = Layer(depth, layer_range)
            self.max_depth = max(self.max_depth, depth)

    def tick(self, steps: int=1, backwards: bool=False):
        self.ticks += -steps if backwards else steps
        for layer in self.layers.values():
            for _ in range(steps):
                layer.tick(1, backwards)
        self.ticks += -steps if backwards else steps

    def can_pass(self, depth: int) -> bool:
        if depth not in self.layers:
            return True

        return self.layers[depth].position != 0

    def reset(self):
        for layer in self.layers.values():
            layer.direction = 1
            layer.position = 0

    def positions(self):
        pos = {}
        for layer in self.layers.values():
            pos[layer.depth] = layer.position
        return pos

    def save(self):
        self.tick_checkpoint = self.ticks

    def rollback(self):
        diff = self.ticks - self.tick_checkpoint
        self.tick(diff, backwards=True)


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
    for delay in count():
        firewall.tick(delay)
        print('Ticks: %d' % firewall.ticks)
        firewall.save()
        if delay % 100 == 0:
            print(delay)
        if not caught_and_reset(firewall):
            return delay
        firewall.rollback()
        print('RB: %d' % firewall.ticks)
