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
    last_played = -1

    # Execute instructions:
    while True:
        instr = instructions[index].split()

        if instr[0] == 'snd':
            last_played = register[instr[1]]
        elif instr[0] == 'set':
            register[instr[1]] = value_of(instr[2])
        elif instr[0] == 'add':
            register[instr[1]] = register.get(instr[1], 0) + value_of(instr[2])
        elif instr[0] == 'mul':
            register[instr[1]] = register.get(instr[1], 0) * value_of(instr[2])
        elif instr[0] == 'mod':
            register[instr[1]] = register.get(instr[1], 0) % value_of(instr[2])
        elif instr[0] == 'rcv':
            freq = register.get(instr[1], 0)
            if freq != 0:
                return last_played
        elif instr[0] == 'jgz':
            if value_of(instr[1]) > 0:
                index += value_of(instr[2]) - 1  # -1: compensates 'index += 1'
        else:
            raise Exception('Unknown instruction: %s' % instr[0])
        index += 1


def solve_part_1(puzzle_input):
    instructions = puzzle_input.split('\n')
    return execute_part_1(instructions)


def execute_part_2(instructions, register=dict()):
    '''Execute instructions for part 2.

    When needing for a value to receive a tuple with amount
    of instructions executed and all sent values will be returned.
    '''
    index = register.get('_INDEX', 0)  # Recover last index
    inbox = register.get('_INBOX', [])
    outbox = list()

    def value_of(name):  # To provide current 'register' by default:
        return value(register, name)

    executed = 0

    # Execute instructions:
    while True:
        instr = instructions[index].split()

        if instr[0] == 'snd':
            outbox.append(value_of(instr[1]))
        elif instr[0] == 'set':
            register[instr[1]] = value_of(instr[2])
        elif instr[0] == 'add':
            register[instr[1]] = register.get(instr[1], 0) + value_of(instr[2])
        elif instr[0] == 'mul':
            register[instr[1]] = register.get(instr[1], 0) * value_of(instr[2])
        elif instr[0] == 'mod':
            register[instr[1]] = register.get(instr[1], 0) % value_of(instr[2])
        elif instr[0] == 'rcv':

            if len(inbox) == 0:
                register['_INDEX'] = index
                return executed, outbox
            register[instr[1]] = inbox.pop(0)

        elif instr[0] == 'jgz':

            if value_of(instr[1]) > 0:
                index += value_of(instr[2]) - 1  # -1: compensates 'index += 1'

        else:
            raise Exception('Unknown instruction: %s' % instr[0])

        index += 1
        executed += 1


def solve_part_2(puzzle_input):
    instructions = puzzle_input.split('\n')

    # Data for both programs:
    prog0_register, prog1_register = {'p': 0}, {'p': 1}
    # Amount of commands executes last time. To detect deadlocks:
    prog0_executions, prog1_executions = -1, -1
    # Current executing program id:
    execute_id = 0

    # Solution for part 2: (counts total values sent from program id 1)
    prog1_sent_total = 0

    # Execute both programs (0 and 1) alternatingly while not deadlocked:
    while prog1_executions != 0 or prog1_executions != 0:
        if execute_id == 0:

            prog0_executions, outbox = execute_part_2(instructions,
                                                      prog0_register)

            # Append to '_INBOX' of prog 1 with the values received from
            # program id 0:
            inbox = prog1_register.get('_INBOX', [])
            prog1_register['_INBOX'] = inbox
            for value in outbox:
                inbox.append(value)

        elif execute_id == 1:
            prog1_executions, outbox = execute_part_2(instructions,
                                                      prog1_register)

            # Append to '_INBOX' of prog 0 with the values received from
            # program id 1:
            inbox = prog0_register.get('_INBOX', [])
            prog0_register['_INBOX'] = inbox
            for value in outbox:
                inbox.append(value)

            # Add sent messages for solution of part 2:
            prog1_sent_total += len(outbox)

        # Switch executing program id ( 0 <-> 1 )
        execute_id = int(not bool(execute_id))

    return prog1_sent_total
