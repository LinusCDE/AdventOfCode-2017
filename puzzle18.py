def execute(instructions):
    register = dict()

    def get_value(name):
        try:
            return int(name)
        except ValueError:
            return register.get(name, 0)

    index = 0
    last_played = -1
    while True:
        instr = instructions[index].split()

        if instr[0] == 'snd':
            last_played = register[instr[1]]
        elif instr[0] == 'set':
            register[instr[1]] = get_value(instr[2])
        elif instr[0] == 'add':
            register[instr[1]] = register.get(instr[1], 0) + get_value(instr[2])
        elif instr[0] == 'mul':
            register[instr[1]] = register.get(instr[1], 0) * get_value(instr[2])
        elif instr[0] == 'mod':
            register[instr[1]] = register.get(instr[1], 0) % get_value(instr[2])
        elif instr[0] == 'rcv':
            freq = register.get(instr[1], 0)
            if freq != 0:
                return last_played
        elif instr[0] == 'jgz':
            if register.get(instr[1], 0) != 0:
                index += get_value(instr[2]) - 1  # -1: compensates 'index += 1'
        else:
            raise Exception('Unknown instruction: %s' % instr[0])
        index += 1


def solve_part_1(puzzle_input):
    instructions = puzzle_input.split('\n')
    return execute(instructions)


def solve_part_2(puzzle_input):
    pass
