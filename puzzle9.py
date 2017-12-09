def process_input(input_str: str, only_yield_garbage=False):
    '''Yields all non garbage or garbage chars (one by one),
    depending on the value of 'only_yield_garbage'.
    Chars with an exclamation mark before ('!') are never yielded.
    '''
    discard_garbage, ignore_next = False, False
    for char in input_str:
        # Handle ignoring of the next char after an exclamation mark ('!'):
        if ignore_next:  # This char has to be ignored
            ignore_next = False  # Disable ignoring
            continue  # Discard this char
        if char is '!':  # This char says that the next one has to be discarded
            ignore_next = True  # Enable ignoring
            continue  # Discard this char
        # --------------------

        # Handle garbage:
        # Everything after '<' is garbage:
        if not discard_garbage and char is '<':
            discard_garbage = True
            continue
        # Everything after '>' is not garbage anymore:
        if discard_garbage and char is '>':
            discard_garbage = False
            continue

        # Output garbage:
        if only_yield_garbage and discard_garbage:
            yield char  # Yield garbage char
        # --------------------

        # Output valid stuff:
        if not only_yield_garbage and not discard_garbage:
            yield char  # Yield valid char


def solve_part_1(puzzle_input):
    score, group_depth = 0, 0
    for char in process_input(puzzle_input):
        if char == '{':  # '{' == group start
            group_depth += 1  # Went one group deeper
            score += group_depth
        elif char == '}':  # '}' == group end
            group_depth -= 1  # Left one group => went one up
    return score


def solve_part_2(puzzle_input):
    garbage_count = 0  # Counts the amount of garbage chars
    for _ in process_input(puzzle_input, only_yield_garbage=True):
        garbage_count += 1
    return garbage_count
