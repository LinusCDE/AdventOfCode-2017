from coordinate_utils import CoordinateField
from puzzle3 import VEC_UP, VEC_RIGHT, VEC_DOWN, VEC_LEFT


print('Hint: Run this puzzle with \'pypy3\' to get vastly improved '
      'performance in part 2.')

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
    The first is a bool that says if the virus infected a node in this burst.
    The second is the new 'directionIdx'.
    '''
    # Decide new direction:
    directionIdx += 1 if cluster[pos] else -1
    directionIdx %= len(DIRECTIONS)

    # Toggle infection:
    infected = cluster[pos] = None if cluster[pos] else True

    # Move one in direction:
    pos[0] += DIRECTIONS[directionIdx][0]
    pos[1] += DIRECTIONS[directionIdx][1]

    return infected, directionIdx


def solve(puzzle_input: str, bursts: int, burst_function: 'function'):
    cluster, pos = load_cluster(puzzle_input)
    directionIdx, count = DIRECTIONS.index(VEC_UP), 0
    log('Starting at: %d, %d' % tuple(pos))

    for _ in range(bursts):
        infected, directionIdx = burst_function(cluster, pos, directionIdx)
        if infected:
            count += 1

    return count


def solve_part_1(puzzle_input):
    return solve(puzzle_input, 10000, burst_function=burst)


def burst_evolved(cluster: CoordinateField, pos: list,
                  directionIdx: int) -> tuple:
    '''Executes one burst for part 2. Changing values in the 'cluster' the
    position ('pos') and returing two values.
    The first is a bool that says if the virus infected a node in this burst.
    The second is the new 'directionIdx'.
    '''
    infected = False

    # Change node values/states and turn depending on them
    node = cluster[pos]
    if not node:  # Clean(ed)
        cluster[pos] = 'W'  # Weaken node
        directionIdx -= 1  # Turn left
    elif node == 'W':  # Weakended
        cluster[pos] = infected = True  # Infect node and remember action
    elif node is True:  # Infected
        cluster[pos] = 'F'  # Flag node
        directionIdx += 1  # Turn right
    elif node == 'F':  # Flagged
        del cluster[pos]  # Clean node
        directionIdx += 2  # Turn around

    directionIdx %= len(DIRECTIONS)

    # Move one in direction:
    pos[0] += DIRECTIONS[directionIdx][0]
    pos[1] += DIRECTIONS[directionIdx][1]

    return infected, directionIdx


def solve_part_2(puzzle_input):
    return solve(puzzle_input, 10000000, burst_function=burst_evolved)
