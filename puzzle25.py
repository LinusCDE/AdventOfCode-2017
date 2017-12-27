import re


print('Hint: Run this puzzle with \'pypy3\' to get vastly improved performance')


class State:
    '''Represents a State in the current AoC puzzle.'''

    def __init__(self, value_for_0: int, value_for_1: int,
                 direction_for_0: int, direction_for_1: int,
                 next_state_for_0: str, next_state_for_1: str):
        self.value_for_0, self.value_for_1 = value_for_0, value_for_1
        self.direction_for_0 = direction_for_0
        self.direction_for_1 = direction_for_1
        self.next_state_for_0 = next_state_for_0
        self.next_state_for_1 = next_state_for_1

    def write(self, tape: set, position: int, value: int):
        '''Writes given 'value' to 'position' at the 'tape'.'''
        if position not in tape and value == 1:
            tape.add(position)
        elif position in tape and value == 0:
            tape.remove(position)

    def invoke(self, tape: set, position: int) -> tuple:
        '''Does its job at the given 'positon' with tape.
        Returns the new postion and the next state.
        '''
        if position not in tape:  # Value at 'postion' == 0
            self.write(tape, position, self.value_for_0)
            position += self.direction_for_0
            next_state = self.next_state_for_0
        else:  # Value at 'postion' == 1
            self.write(tape, position, self.value_for_1)
            position += self.direction_for_1
            next_state = self.next_state_for_1

        return position, next_state


def load_states(input_lines: list) -> dict:
    '''Reads and returns all states in 'input_lines'.'''
    states = {}
    state_begin_pattern = re.compile('In state [A-Z]:')

    for index, line in enumerate(input_lines):
        if not state_begin_pattern.match(line):
            continue

        # Read data:
        name = line[-2]
        value_for_0 = int(input_lines[index + 2][-2])
        dir_for_0 = 1 if input_lines[index + 3].split()[-1] == 'right.' else -1
        next_state_for_0 = input_lines[index + 4][-2]
        value_for_1 = int(input_lines[index + 6][-2])
        dir_for_1 = 1 if input_lines[index + 7].split()[-1] == 'right.' else -1
        next_state_for_1 = input_lines[index + 8][-2]

        # Add a state:
        states[name] = State(value_for_0, value_for_1,
                             dir_for_0, dir_for_1,
                             next_state_for_0, next_state_for_1)

    return states


def begin_name_and_checksum(input_lines: list):
    '''Returns first state name and the target checksum point.'''
    return input_lines[0][-2], int(input_lines[1].split()[-2])


def solve_part_1(puzzle_input):
    # Load and parse input data:
    input_lines = puzzle_input.split('\n')
    state_name, checksum_count = begin_name_and_checksum(input_lines)
    states = load_states(input_lines)

    tape = set()  # If an number is in the set the value for this postion is 1
    position = 0

    for _ in range(checksum_count):
        position, state_name = states[state_name].invoke(tape, position)

    return len(tape)  # Tape contains only postions that are 1
