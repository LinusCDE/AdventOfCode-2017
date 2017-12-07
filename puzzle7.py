import json


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


def get_weight_sum(prog_name, held, weight_data):
    if len(held[prog_name]) > 0:
        progs = held[prog_name]
        sub_progs_sum = sum(map(lambda prog: get_weight_sum(prog, held, weight_data), progs))
        return weight_data[prog_name] + sub_progs_sum
    else:
        return weight_data[prog_name]


def to_node(prog_name, held, weight_data, attach_to=dict()):
    result = {}

    # Add Weight info:
    total_weight = get_weight_sum(prog_name, held, weight_data)
    self_weight = weight_data[prog_name]
    result['WEIGHT'] = self_weight
    if self_weight != total_weight:
        result['TOTAL_WEIGHT'] = total_weight

    # Add Subprograms recursivly:
    sub_progs = held.get(prog_name, [])
    sub_progs_weights = list()
    for sub_prog in sub_progs:
        to_node(sub_prog, held, weight_data, attach_to=result)
        if isinstance(result[sub_prog], dict):
            sub_dat = result[sub_prog]
            sub_progs_weights.append(sub_dat['TOTAL_WEIGHT'] if 'TOTAL_WEIGHT' in sub_dat else sub_dat['WEIGHT'])
        elif isinstance(result[sub_prog], int):
            sub_progs_weights.append(result[sub_prog])
        else:
            sub_progs_weights.append(int(result[sub_prog].split(' / ')[1]))
    if minority(sub_progs_weights) is not None:
        result['UNBLANCED'] = True
    else:
        result = '%d / %d' % (self_weight, total_weight)

    # Only weight as value if no recursion available:
    if isinstance(result, dict) and len(result) is 1:
        result = result['WEIGHT']

    # Attach to given dict:
    attach_to[prog_name] = result
    return attach_to


def solve_part_2(puzzle_input):
    prog_toplevel, held, weight_data = parse_data(puzzle_input)
    structure = to_node(prog_toplevel, held, weight_data)
    print('"%s":' % prog_toplevel)
    print(json.dumps(structure[prog_toplevel], indent=4, sort_keys=False))
