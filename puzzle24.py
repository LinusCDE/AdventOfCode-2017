print('Hint: Run this puzzle with \'pypy3\' to get vastly improved performance')


class Component:

    def __init__(self, identifier: int, left_type: int, right_type: int):
        self.identifier = identifier
        self.left_type, self.right_type = left_type, right_type
        self.swapped = False

    def __str__(self):
        return '%d/%d' % (self.left_type, self.right_type)

    def __hash__(self):
        return self.identifier

    def swap(self):
        self.left_type, self.right_type = self.right_type, self.left_type
        self.swapped = not self.swapped

    def reset(self):
        if self.swapped:
            self.swap()


def load_components(puzzle_input) -> list:
    components = []

    for identifier, line in enumerate(puzzle_input.split('\n')):
        port1, port2 = map(int, line.split('/'))
        components.append(Component(identifier, port1, port2))

    return components


def build(remaining: set, current_bridge: list=list(), found: list=list()):
    for component in remaining:
        component.reset()

    last_component = current_bridge[-1] if len(current_bridge) > 0 else Component(-1, 999, 0)
    for possible in remaining:

        ok = False
        if possible.left_type == last_component.right_type:
            ok = True
        else:
            possible.swap()
            if possible.left_type == last_component.right_type:
                ok = True

        if ok:
            new_bridge = list(current_bridge)
            new_remain = set(remaining)
            new_bridge.append(possible)
            new_remain.remove(possible)

            found.append(list(new_bridge))
            build(new_remain, new_bridge, found)

    return found


def strenght_of(bridge: list):
    strenght = 0
    for component in bridge:
        strenght += component.left_type + component.right_type
    return strenght


def solve_part_1(puzzle_input):
    components = set(load_components(puzzle_input))
    bridges = build(components)  # Possible bridges

    best = max(bridges, key=lambda bridge: strenght_of(bridge))
    log('Best bridge: %s' % '--'.join(map(str, best)))
    return strenght_of(best)


def solve_part_2(puzzle_input):
    components = set(load_components(puzzle_input))
    bridges = build(components)  # Possible bridges

    best = []
    best_stenght = 0
    best_length = 0
    for bridge in bridges:
        this_length = len(bridge)
        this_strength = strenght_of(bridge)

        if this_length > best_length \
           or (this_length == best_length and this_strength > best_stenght):
            best, best_stenght, best_length = bridge, this_strength, this_length

    log('Best longest bridge: %s' % '--'.join(map(str, best)))
    return strenght_of(best)
