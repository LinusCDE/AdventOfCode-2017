import re


print('Hint: Run this puzzle with \'pypy3\' to get vastly improved performance')


class State:

    def __init__(self, value_for_0: int, value_for_1: int,
                 direction_for_0: int, direction_for_1: int,
                 next_state_for_0: str, next_state_for_1: str):
        self.value_for_0, self.value_for_1 = value_for_0, value_for_1
        self.direction_for_0 = direction_for_0
        self.direction_for_1 = direction_for_1
        self.next_state_for_0 = next_state_for_0
        self.next_state_for_1 = next_state_for_1

        #print(locals())

    def write(self, tape: set, position: int, value: int):
        #print('Value: %s, Position: %s' % (value, position))
        if position not in tape and str(value) == '1':
            #print('Put 1 to %d' % position)
            tape.add(position)
            #print(tape)
        elif position in tape and str(value) == '0':
            #print('Put 0 to %d' % position)
            tape.remove(position)

    def invoke(self, tape: set, position: int) -> tuple:
        if position not in tape:  # Value == 0
            self.write(tape, position, self.value_for_0)
            position += self.direction_for_0
            next_state = self.next_state_for_0
        else:
            self.write(tape, position, self.value_for_1)
            position += self.direction_for_1
            next_state = self.next_state_for_1

        return position, next_state


def load_states(input_lines: list) -> dict:
    states = {}
    state_begin_pattern = re.compile('In state [A-Z]:')

    for index, line in enumerate(input_lines):
        if not state_begin_pattern.match(line):
            continue

        name = line[-2]

        value_for_0 = input_lines[index + 2][-2]
        dir_for_0 = 1 if input_lines[index + 3].split()[-1] == 'right.' else -1
        next_state_for_0 = input_lines[index + 4][-2]

        value_for_1 = input_lines[index + 6][-2]
        dir_for_1 = 1 if input_lines[index + 7].split()[-1] == 'right.' else -1
        next_state_for_1 = input_lines[index + 8][-2]

        states[name] = State(value_for_0, value_for_1,
                             dir_for_0, dir_for_1,
                             next_state_for_0, next_state_for_1)

    return states


def begin_name_and_checksum(input_lines: list):
    return input_lines[0][-2], int(input_lines[1].split()[-2])


def solve_part_1(puzzle_input):
    input_lines = puzzle_input.split('\n')
    state_name, checksum_count = begin_name_and_checksum(input_lines)
    states = load_states(input_lines)

    tape = set()
    position = 0

    for _ in range(checksum_count):
        #print('State %s' % state_name)
        position, state_name = states[state_name].invoke(tape, position)
        #print('Step %d. About to run :' % (_+1), state_name)
        #for pos in range(-3, 4):
        #    val = 1 if pos in tape else 0
        #    if pos == position:
        #        val = '[%d]' % val
        #    else:
        #        val = ' %d ' % val
        #    print('%s ' % val, end='')
        #print()

    return len(tape)


def solve_part_2(puzzle_input):
    pass
