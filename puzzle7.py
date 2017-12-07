class Solution(Exception):  # Misuse of exception handling

    def __init__(self, solution):
        Exception.__init__(self)
        self.solution = solution


def parse_data(puzzle_input: str) -> tuple:
    weight = {}  # Format: {prog1, weight1, prog2: weight2, ...}
    held = {}  # Format: {prog1: [prog2, prog3, ...], ...}
    for line in puzzle_input.split('\n'):
        prog_name, holding = None, []
        if ' -> ' in line:
            line = line.split(' -> ')
            prog_name = line[0]
            holding = line[1].split(', ') if ', ' in line[1] else [line[1]]
        else:
            prog_name = line.strip()
        splitted = prog_name.split(' (')
        prog_name = splitted[0]
        held[prog_name] = holding
        weight[prog_name] = int(splitted[1][:-1])

    possibles = list(held.keys())
    for holding in held.values():
        for prog in holding:
            possibles.remove(prog)
    if len(possibles) is not 1:
        raise Exception('Only one remaining program expected!')
    return possibles[0], held, weight


def solve_part_1(puzzle_input):
    return parse_data(puzzle_input)[0]


def minority(elms) -> int:
    if len(elms) is 0:
        return None
    elm_count = {}  # Format: {value: count}
    for elm in elms:
        elm_count[elm] = elm_count.get(elm, 0) + 1
    if elms[0] * len(elms) == sum(elm_count.values()):  # No minority
        return None
    return min(elms, key=lambda elm: elm_count[elm])


def get_weight(prog_name, held, weight):
    if prog_name in held:
        progs = held[prog_name]
        return sum(map(lambda prog: get_weight(prog, held, weight), progs))
    else:
        return weight[prog_name]


def solve_part_2(puzzle_input):
    prog_toplevel, held, weight = parse_data(puzzle_input)
    # Strip all empty lists from 'held':
    for prog_name in tuple(held.keys()):
        if len(held[prog_name]) is 0:
            del held[prog_name]
    for progs_on_disk in held.values():
        weights = tuple(get_weight(prog) for prog in progs_on_disk)
        fault = minority(weights)
        if fault:
            
    return None
