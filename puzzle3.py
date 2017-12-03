log = None


def distance(pos1, pos2):
    pos_new = [max(pos1[0], pos2[0]) - min(pos1[0], pos2[0]), max(pos1[1], pos2[1]) - min(pos1[1], pos2[1])]
    return sum(pos_new)


def spiral_generator():
    len_x, len_y = 1, 0
    cur_dir = [1, 0]
    remain = 1
    pos = [0, 0]
    yield pos
    while True:
        pos[0], pos[1] = pos[0] + cur_dir[0], pos[1] + cur_dir[1]
        yield pos
        remain -= 1
        if remain is 0:
            if cur_dir == [1, 0]:
                cur_dir = [0, -1]
                len_y += 1
            elif cur_dir == [0, -1]:
                cur_dir = [-1, 0]
                len_x += 1
            elif cur_dir == [-1, 0]:
                cur_dir = [0, 1]
                len_y += 1
            elif cur_dir == [0, 1]:
                cur_dir = [1, 0]
                len_x += 1
            remain = distance(pos, [pos[0] + (len_x * cur_dir[0]), pos[1] + (len_y * cur_dir[1])])


def get_adjecent(pos):
    for y in range(-1, 2):
        for x in range(-1, 2):
            yield (pos[0] + y, pos[1] + x)


def solve_part_1(puzzle_input):
    target_index = int(puzzle_input) - 1
    log('Target is: %d' % (target_index + 1))
    for index, pos in enumerate(spiral_generator()):
        if index == target_index:
            log('Target Position: %s' % pos)
            return distance([0, 0], pos)


def solve_part_2(puzzle_input):
    puzzle_input = int(puzzle_input)
    values = {(0, 0): 1}  # (x, y): value
    for index, pos in enumerate(spiral_generator()):
        value = 0
        for adjecent_pos in get_adjecent(pos):
            if adjecent_pos in values:
                value += values[adjecent_pos]
        log('Pos: %s has value %d' % (pos, value))
        values[tuple(pos)] = value
        if value > puzzle_input:
            log('Target Position: %s' % pos)
            return value
