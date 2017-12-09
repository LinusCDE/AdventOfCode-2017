from io import StringIO


garbage = 0


def discard_garbage(input_string):
    global garbage
    discarding, ignore_next = False, False
    for char in input_string:
        if ignore_next:
            ignore_next = False
            continue
        if char is '!':
            ignore_next = True
            continue
        if discarding and char is not '>':
            garbage += 1
        if char is '<':
            discarding = True
            continue
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
    for _ in discard_garbage(puzzle_input):
        pass
    return garbage
