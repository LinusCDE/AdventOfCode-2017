def execute_sound_instructions(instructions):
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
    return execute_sound_instructions(instructions)


def execute_part_2(instructions, register=dict()):
    index = register.get('_INDEX', 0)  # Recover last index
    inbox = register.get('_INBOX', [])
    outbox = list()

    executed = 0

    def get_value(name):
        try:
            return int(name)
        except ValueError:
            return register.get(name, 0)

    while True:
        instr = instructions[index].split()

        if instr[0] == 'snd':
            outbox.append(get_value(instr[1]))
        elif instr[0] == 'set':
            register[instr[1]] = get_value(instr[2])
        elif instr[0] == 'add':
            register[instr[1]] = register.get(instr[1], 0) + get_value(instr[2])
        elif instr[0] == 'mul':
            register[instr[1]] = register.get(instr[1], 0) * get_value(instr[2])
        elif instr[0] == 'mod':
            register[instr[1]] = register.get(instr[1], 0) % get_value(instr[2])
        elif instr[0] == 'rcv':
            if len(inbox) == 0:
                register['_INDEX'] = index
                return executed, outbox
            register[instr[1]] = inbox.pop(0)
        elif instr[0] == 'jgz':
            if register.get(instr[1], 0) != 0:
                index += get_value(instr[2]) - 1  # -1: compensates 'index += 1'
        else:
            raise Exception('Unknown instruction: %s' % instr[0])
        index += 1
        executed += 1


def solve_part_2(puzzle_input):
    instructions = puzzle_input.split('\n')

    prog0_register, prog1_register = {'p': 0}, {'p': 1}
    prog0_executions, prog1_executions = -1, -1
    execute_id = 0

    prog1_sent_total = 0

    while prog1_executions != 0 or prog1_executions != 0:
        print('Executing program %d' % execute_id)
        if execute_id == 0:
            prog0_executions, outbox = execute_part_2(instructions,
                                                      prog0_register)
            inbox = prog1_register.get('_INBOX', [])
            prog1_register['_INBOX'] = inbox
            for value in outbox:
                inbox.append(value)
            execute_id = 1
        elif execute_id == 1:
            prog1_executions, outbox = execute_part_2(instructions,
                                                      prog1_register)
            inbox = prog0_register.get('_INBOX', [])
            prog0_register['_INBOX'] = inbox
            for value in outbox:
                inbox.append(value)
            prog1_sent_total += len(outbox)
            print('Solution so far: %d' % prog1_sent_total)
            execute_id = 0

    return prog1_sent_total
