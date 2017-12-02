from itertools import permutations

log = None


def get_rows(puzzle_input):
    return tuple(puzzle_input.split('\n'))


def solve_part_1(puzzle_input):
    checksum_total = 0
    puzzle_input = puzzle_input.replace(' ', '\t')
    for row in get_rows(puzzle_input):
        entries = list(int(val) for val in row.split('\t'))
        entries.sort()
        checksum = (entries[-1] - entries[0])
        log('Checksum: %d' % checksum)
        checksum_total += checksum
    return checksum_total


def solve_part_2(puzzle_input):
    checksum_total = 0
    puzzle_input = puzzle_input.replace(' ', '\t')
    for row in get_rows(puzzle_input):
        entries = list(int(val) for val in row.split('\t'))
        entries.sort()
        checksum = 0
        for v1, v2 in permutations(entries, 2):
            if v1 % v2 is 0:
                checksum = v1 // v2
        log('Checksum: %d' % checksum)
        checksum_total += checksum
    return checksum_total
