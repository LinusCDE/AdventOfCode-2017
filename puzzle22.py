from coordinate_utils import CoordinateField
from puzzle3 import VEC_UP, VEC_RIGHT, VEC_DOWN, VEC_LEFT


DIRECTIONS = (VEC_UP, VEC_RIGHT, VEC_DOWN, VEC_LEFT)


def load_cluster(puzzle_input: str) -> tuple:
    '''Returns a tuple with the coordinatefield and the
    start position (as list).
    '''
    cluster = CoordinateField()
    start_width, start_height = 0, 0

    puzzle_input = puzzle_input.replace(' ', '')  # To work with the test input

    for y, line in enumerate(puzzle_input.split('\n')):
        start_height += 1
        if start_width == 0:
            start_width = len(line)

        for x, _ in filter((lambda x_v: x_v[1] == '#'), enumerate(line)):
            cluster[x, y] = True

    return cluster, [start_width // 2, start_height // 2]


def burst(cluster: CoordinateField, pos: list, directionIdx: int) -> tuple:
    '''Executes one burst. Changing values in the 'cluster' the
    position ('pos') and returing two values.
    The first is a bool that says if the virus infected a cell in this burst.
    The seconds is the new 'directionIdx'.
    '''
    directionIdx += 1 if cluster[pos] else -1
    directionIdx %= len(DIRECTIONS)

    infected = False

    if cluster[pos]:
        del cluster[pos]
    else:
        cluster[pos] = infected = True

    pos[0] += DIRECTIONS[directionIdx][0]
    pos[1] += DIRECTIONS[directionIdx][1]

    return infected, directionIdx


def solve_part_1(puzzle_input):
    cluster, pos = load_cluster(puzzle_input)
    directionIdx = DIRECTIONS.index(VEC_UP)
    log('Starting at: %d, %d' % tuple(pos))

    count = 0

    for _ in range(10000):
        infected, directionIdx = burst(cluster, pos, directionIdx)
        if infected:
            count += 1

    return count


def solve_part_2(puzzle_input):
    pass
