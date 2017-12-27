def value(register, name):
    '''Return value from 'register' or parse 'name' to int if already a one.'''
    try:
        return int(name)
    except ValueError:
        return register.get(name, 0)


def execute_part_1(instructions):
    '''Execute instructions for part 1. Returning recovered frequency.'''
    register = dict()

    def value_of(name):  # To provide current 'register' by default:
        return value(register, name)

    index = 0
    mul_count = 0

    # Execute instructions:
    while index >= 0 and index < len(instructions):
        instr = instructions[index].split()

        if instr[0] == 'set':
            register[instr[1]] = value_of(instr[2])
        elif instr[0] == 'sub':
            register[instr[1]] = register.get(instr[1], 0) - value_of(instr[2])
        elif instr[0] == 'mul':
            mul_count += 1
            register[instr[1]] = register.get(instr[1], 0) * value_of(instr[2])
        elif instr[0] == 'jnz':
            if value_of(instr[1]) != 0:
                index += value_of(instr[2]) - 1  # -1: compensates 'index += 1'
        else:
            raise Exception('Unknown instruction: %s' % instr[0])
        index += 1

    return mul_count


def solve_part_1(puzzle_input):
    instructions = puzzle_input.split('\n')
    return execute_part_1(instructions)
