from io import StringIO


def discard_weight(input_string):
    out, discarding = StringIO(), False
    for char in input_string:
        if char is '(':
            discarding = True
        if not discarding:
            out.write(char)
        if char is ')':
            discarding = False
    val = out.getvalue()
    out.close()
    return val


def solve_part_1(puzzle_input):
    puzzle_input = discard_weight(puzzle_input)
    held = {}  # Format: {prog1: [prog2, prog3, ...], ...}
    for line in puzzle_input.split('\n'):
        prog_name, holding = None, []
        if '  -> ' in line:
            line = line.split('  -> ')
            prog_name = line[0]
            holding = line[1].split(', ') if ', ' in line[1] else [line[1]]
        else:
            prog_name = line.strip()
        held[prog_name] = holding

    possibles = list(held.keys())
    for holding in held.values():
        for prog in holding:
            possibles.remove(prog)
    if len(possibles) is not 1:
        raise Exception('Only one remaining program expected!')
    return possibles[0]


def solve_part_2(puzzle_input):
    pass
