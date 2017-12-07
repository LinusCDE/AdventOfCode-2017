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
    last_count = None
    for count in elm_count.values():
        if last_count is None:
            last_count = count
        if count != last_count:
            break
    else:
        return None  # No minority available
    return min(elms, key=lambda elm: elm_count[elm])


def get_weight(prog_name, held, weight_data):
    if prog_name in held:
        progs = held[prog_name]
        return weight_data[prog_name] + sum(map(lambda prog: get_weight(prog, held, weight_data), progs))
    else:
        return weight_data[prog_name]


def solve_part_2(puzzle_input):
    prog_toplevel, held, weight_data = parse_data(puzzle_input)
    # Strip all empty lists from 'held':
    for prog_name in tuple(held.keys()):
        if len(held[prog_name]) is 0:
            del held[prog_name]
    if True:
        progs = held[prog_toplevel]
        weights = tuple(get_weight(prog, held, weight_data) for prog in progs)
        fault, fault_prog = minority(weights), None
        correct_weight = None
        if fault is not None:  # Find faulty program
            log('--------------------')
            for prog, weight in zip(progs, weights):
                log('%s: %d' %(prog, weight))
                if weight == fault:
                    fault_prog = prog
                else:
                    correct_weight = weight
            weight_self = weight_data[fault_prog]
            diff = fault - correct_weight
            corr = weight_self - diff
            log('%s has a faulty weight of %d.' % (fault_prog, fault))
            return corr
    return None
