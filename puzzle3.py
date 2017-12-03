log = None


def distance(pos1, pos2):
    x_dist = max(pos1[0], pos2[0]) - min(pos1[0], pos2[0])
    y_dist = max(pos1[1], pos2[1]) - min(pos1[1], pos2[1])
    return x_dist + y_dist


# Directions as coordinates/vectors:
VEC_UP = (0, -1)
VEC_LEFT = (-1, 0)
VEC_DOWN = (0, 1)
VEC_RIGHT = (1, 0)


def spiral():
    '''This outputs every next position of the spiral.'''
    width, height = 1, 0
    vec = VEC_RIGHT
    remain = 1
    pos = (0, 0)  # Starting point of the spiral
    yield pos
    while True:
        pos = pos[0] + vec[0], pos[1] + vec[1]  # Go one into cur_dir
        yield pos
        remain -= 1
        if remain is 0:  # Turn left (spiral direction)
            if vec == VEC_RIGHT:
                vec = VEC_UP
                height += 1
            elif vec == VEC_UP:
                vec = VEC_LEFT
                width += 1
            elif vec == VEC_LEFT:
                vec = VEC_DOWN
                height += 1
            elif vec == VEC_DOWN:
                vec = VEC_RIGHT
                width += 1
            target_pos = (pos[0] + (width * vec[0]), pos[1] + (height * vec[1]))
            remain = distance(pos, target_pos)


def solve_part_1(puzzle_input):
    target_index = int(puzzle_input) - 1
    log('Target is: %d' % (target_index + 1))
    for index, pos in enumerate(spiral()):
        if index == target_index:
            log('Target Position: %s' % str(pos))
            return distance([0, 0], pos)


def adjecents(pos):
    for y in range(-1, 2):  # -> -1, 0, 1
        for x in range(-1, 2):  # -> -1, 0, 1
            yield pos[0] + y, pos[1] + x


def put_value(infinite_matrix: dict, pos: tuple, value):
    if pos[0] not in infinite_matrix:  # Create dict for y-values
        infinite_matrix[pos[0]] = {}
    infinite_matrix[pos[0]][pos[1]] = value


def get_value(infinite_matrix: dict, pos: tuple):
    # Check if coordante is existing:
    if pos[0] not in infinite_matrix or pos[1] not in infinite_matrix[pos[0]]:
        return None
    return infinite_matrix[pos[0]][pos[1]]


def solve_part_2(puzzle_input):
    puzzle_input = int(puzzle_input)
    values = {}  # infinite_matrix (used with the two functions above)
    put_value(values, (0, 0), 1)
    for index, pos in enumerate(spiral()):
        value = 0
        for adjecent_pos in adjecents(pos):
            adjecent_pos_value = get_value(values, adjecent_pos)
            if adjecent_pos_value:
                value += adjecent_pos_value
        if value > puzzle_input:
            log('Target Position: %s' % str(pos))
            return value
        put_value(values, pos, value)
