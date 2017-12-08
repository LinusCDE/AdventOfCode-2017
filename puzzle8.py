def compare(first_value: int, operator: str, second_value: int) -> bool:
    '''Compare two values.
    This is more than 10 times faster than eval()
    '''
    if operator == '>=':
        return first_value >= second_value
    elif operator == '>':
        return first_value > second_value
    elif operator == '==':
        return first_value == second_value
    elif operator == '<=':
        return first_value <= second_value
    elif operator == '<':
        return first_value < second_value
    elif operator == '!=':
        return first_value != second_value


def execute(line: str, register: dict) -> int:
    '''Executes the instruction
    and returns the value for the changed register.
    If it wasn't executed, 0 will be returned.
    '''
    # Get all data: ('op' is shorthand for 'operator')
    do_name, do_op, do_value, _, when_name, when_op, when_value = line.split()
    do_value, when_value = int(do_value), int(when_value)

    if(compare(register.get(when_name, 0), when_op, when_value)):
        if do_op == 'dec':  # Invert value if decrementing
            do_value *= -1
        # Do operation on register
        register[do_name] = ret = register.get(do_name, 0) + do_value
        return ret
    return 0


def solve_part_1(puzzle_input):
    register = {}
    for line in puzzle_input.split('\n'):
        execute(line, register)
    return max(register.values())


def solve_part_2(puzzle_input):
    register, highest = {}, 0
    for line in puzzle_input.split('\n'):
        highest = max(execute(line, register), highest)
    return highest
