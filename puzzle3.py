def distance(pos1: tuple, pos2: tuple):
    '''Returns the Manhattan distance of two points.'''
    # Scheme: n_dist = (p1N - p2N) if (p1N > p2N) else (p2N - p1N)
    x_dist = pos1[0] - pos2[0] if pos1[0] > pos2[0] else pos2[0] - pos1[0]
    y_dist = pos1[1] - pos2[1] if pos1[1] > pos2[1] else pos2[1] - pos1[1]
    return x_dist + y_dist


# Coordinate system is like the one of a monitor
# Directions as coordinates/vectors:
VEC_UP = (0, -1)
VEC_LEFT = (-1, 0)
VEC_DOWN = (0, 1)
VEC_RIGHT = (1, 0)


def vector_turn_left(vec: tuple):
    '''Returns the next vector that is pointing leftwards of the given one.'''
    if vec is VEC_RIGHT:
        return VEC_UP
    elif vec is VEC_UP:
        return VEC_LEFT
    elif vec is VEC_LEFT:
        return VEC_DOWN
    elif vec is VEC_DOWN:
        return VEC_RIGHT
    else:
        raise Exception('Invalid Vector!')


def spiral(skip_to_step=None):
    '''Generates all positions of the spiral. If 'skip_to_step' is given,
    all positions except the final position to be about 57 times faster
    with the given puzzle_input.'''
    pos, vec, width, height, remain = (0, 0), VEC_RIGHT, 1, 0, 1
    if not skip_to_step:
        yield pos

    if skip_to_step == 1:  # To prevent step 1 from beeing skipped
        yield pos
        return

    # Only necessary for the use of 'skip_to_step':
    target_pos, step = None, 1
    while True:
        # Skip steps if allowed and below the target step (skip_to_step):
        if target_pos and skip_to_step and step + remain <= skip_to_step:
            step += remain
            remain = 0
            pos = target_pos
        else:
            pos = pos[0] + vec[0], pos[1] + vec[1]  # Go one step
            step += 1
            remain -= 1
            if not skip_to_step:
                yield pos

        # Return last pos and end generator when target step is reached:
        if skip_to_step == step:  # The 'is'-operator will not work here
            yield pos
            return  # End generator

        if remain is 0:  # Turn left (spiral direction)
            vec = vector_turn_left(vec)
            if vec[0] is not 0:  # Vector is left or right
                width += 1
            elif vec[1] is not 0:  # Vector is up or down
                height += 1

            target_pos = (pos[0] + (width * vec[0]), pos[1] + (height * vec[1]))
            remain = distance(pos, target_pos)


def solve_part_1(puzzle_input):
    target_step = int(puzzle_input)
    return distance((0, 0), next(spiral(skip_to_step=target_step)))


def adjecents_of(pos: tuple):
    '''Generates all positions around a given one.'''
    for y in range(-1, 2):  # -> -1, 0, 1
        for x in range(-1, 2):  # -> -1, 0, 1
            yield pos[0] + y, pos[1] + x


def put_value(infinite_matrix: dict, pos: tuple, value):
    '''Puts value into a 2D-Dict with no fixed size (called infinite_matrix)'''
    if pos[0] not in infinite_matrix:  # Create dict for y-values
        infinite_matrix[pos[0]] = {}
    infinite_matrix[pos[0]][pos[1]] = value


def get_value(infinite_matrix: dict, pos: tuple):
    '''Retreives value from the 'infinite_matrix'.'''
    # Check if coordante is existing:
    if pos[0] not in infinite_matrix or pos[1] not in infinite_matrix[pos[0]]:
        return None
    return infinite_matrix[pos[0]][pos[1]]


def solve_part_2(puzzle_input):
    puzzle_input = int(puzzle_input)
    values = {}  # infinite_matrix (used with the two functions above)
    put_value(values, (0, 0), 1)
    for index, pos in enumerate(spiral()):
        value_sum = 0  # Sum of the values of all adjecent positions
        for adjecent_pos in adjecents_of(pos):
            adj_value = get_value(values, adjecent_pos)
            if adj_value:
                value_sum += adj_value
        if value_sum > puzzle_input:
            return value_sum
        put_value(values, pos, value_sum)
