log = None

# Coordinate System:
# W (-) --> x --> E (+)
# N (-) --> y --> S (+)


def steps_to(ta_pos: list) -> int:
    '''Walks to the target position and returns the needed steps.'''
    pos, steps = [0, 0], 0
    while pos != ta_pos:  # While not at target position
        north_south = ''  # Will contain either 'n' or 's'
        if ta_pos[1] > pos[1]:  # Target is south to the current position
            north_south = 's'
        else:  # Target is north or on same longitude as the current position
            north_south = 'n'

        east_west = ''  # Will contain either 'e', 'w' or ''
        if ta_pos[0] > pos[0]:
            east_west = 'e'
        elif ta_pos[0] < pos[0]:
            east_west = 'w'

        move(pos, north_south + east_west)
        steps += 1
    return steps


def move(pos: list, direction: str):
    '''Moves given 'pos' one step into the given 'direction'.'''
    if direction == 'n':
        pos[1] -= 1  # North
    elif direction == 's':
        pos[1] += 1  # South
    elif direction == 'nw':
        pos[0] -= 1  # West
        pos[1] -= .5  # half North
    elif direction == 'ne':
        pos[0] += 1  # East
        pos[1] -= .5  # half North
    elif direction == 'sw':
        pos[0] -= 1  # West
        pos[1] += .5  # half South
    elif direction == 'se':
        pos[0] += 1  # East
        pos[1] += .5  # half South
    else:
        raise Exception('Invalid direction: %d' % direction)


def solve_part_1(puzzle_input):
    pos = [0, 0]  # Starting point
    # Move to proccess all instructions:
    for direction in puzzle_input.split(','):
        move(pos, direction)
    log('Target Position: %d, %d' % (pos[0], pos[1]))
    # Return the steps for getting to this position:
    return steps_to(pos)


def solve_part_2(puzzle_input):
    pos = [0, 0]  # Starting point
    most_steps = -1  # The most steps to the target:
    for direction in puzzle_input.split(','):
        move(pos, direction)
        steps = steps_to(pos)
        most_steps = max(most_steps, steps)
    return most_steps
