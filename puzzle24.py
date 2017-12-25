print('Hint: Run this puzzle with \'pypy3\' to get vastly improved performance')


class Component:
    '''Represents a component in the AoC puzzle (obvious).'''

    def __init__(self, identifier: int, left_type: int, right_type: int):
        self.identifier = identifier
        self.left_type, self.right_type = left_type, right_type
        self.swapped = False  # Whether the ports are currently swapped

    def __str__(self):
        return '%d/%d' % (self.left_type, self.right_type)

    def __hash__(self):
        return self.identifier

    def swap(self):
        '''Swaps both ports (= 'self.left_type' and 'self.right_type').'''
        self.left_type, self.right_type = self.right_type, self.left_type
        self.swapped = not self.swapped

    def reset(self):
        '''Restores the original positions of the ports.'''
        if self.swapped:
            self.swap()


def load_components(puzzle_input) -> list:
    '''Returns a list of Components for the given 'puzzle_input'.'''
    components = []

    for identifier, line in enumerate(puzzle_input.split('\n')):
        port1, port2 = map(int, line.split('/'))
        components.append(Component(identifier, port1, port2))

    return components


def build(remaining: set, current_bridge: list=list(),
          found: list=list()) -> list:
    '''Builds all valid bridges recursivly and returns them as a list
    containing lists with Components (they may be in swapped state).
    Also adds them to 'found' as well.

    Should only be called with 'remaining' containing a set of all components.
    '''

    # Unswapp all Components that are not in the current bridge:
    for component in remaining:
        component.reset()

    # If not last component, a fitting one for the first will be assumed:
    last_component = current_bridge[-1] if len(current_bridge) > 0 else Component(-1, 999, 0)

    for possible in remaining:  # Iterate next possible components

        fitting = False
        if last_component.right_type == possible.left_type:
            fitting = True
        elif last_component.right_type == possible.right_type:
            possible.swap()
            fitting = True

        if not fitting:
            continue

        # Found a fitting component => New bridge to add to 'found':
        new_bridge = current_bridge + [possible]
        found.append(new_bridge)

        new_remaining = set(remaining)
        new_remaining.remove(possible)

        # Recursivly continue building bridge based on current one:
        build(new_remaining, new_bridge, found)

    return found  # All found bridges


def strength_of(bridge: list):
    '''Calculates the strength of given 'bridge'.'''
    strength = 0
    for component in bridge:
        strength += component.left_type + component.right_type

    return strength


def solve_part_1(puzzle_input):
    components = set(load_components(puzzle_input))

    bridges = build(components)
    best = max(bridges, key=lambda bridge: strength_of(bridge))

    log('Strongest bridge: %s' % '--'.join(map(str, best)))
    return strength_of(best)


def solve_part_2(puzzle_input):
    components = set(load_components(puzzle_input))

    bridges = build(components)  # Possible bridges
    # Max of primary longest and secondary strongest bridge:
    best = max(bridges, key=lambda bridge: (len(bridge), strength_of(bridge)))

    log('Strongest and longest bridge: %s' % '--'.join(map(str, best)))
    return strength_of(best)
