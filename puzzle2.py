from itertools import permutations

log = None


def solve_part_1(puzzle_input):
    checksum_total = 0
    puzzle_input = puzzle_input.replace(' ', '\t')  # Helpful for the examples
    for row in puzzle_input.split('\n'):
        entries = tuple(map(int, row.split('\t')))  # Entries as ints
        checksum_row = (max(entries) - min(entries))  # + checksum for cur. row
        log('Row-Checksum: %d' % checksum_row)
        checksum_total += checksum_row
    return checksum_total  # The solution is the total of all checksums


def solve_part_2(puzzle_input):
    checksum_total = 0
    puzzle_input = puzzle_input.replace(' ', '\t')  # Helpful for the examples
    for row in puzzle_input.split('\n'):
        entries = tuple(map(int, row.split('\t')))   # Entries as ints
        for entry1, entry2 in permutations(entries, 2):
            if entry1 % entry2 is 0:
                checksum_row = entry1 // entry2  # + checksum for cur. row
                break
        else:  # If no checksum found:
            raise Exception('Could not find any checksum for row: "%s"' % row)
        log('Row-Checksum: %d' % checksum_row)
        checksum_total += checksum_row
    return checksum_total  # The solution is the total of all checksums
