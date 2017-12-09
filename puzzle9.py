from io import StringIO


def discard_garbage(input_string):
    discarding, ignore_next = False, False
    for char in input_string:
        if ignore_next:
            ignore_next = False
            continue
        if char is '!':
            ignore_next = True
            continue
        if char is '<':
            discarding = True
        if not discarding:
            yield char
        if char is '>':
            discarding = False


def solve_part_1(puzzle_input):
    score, level = 0, 0
    for char in discard_garbage(puzzle_input):
        if char == '{':
            level += 1
            score += level
        elif char == '}':
            level -= 1
    return score


def solve_part_2(puzzle_input):
    pass
