from itertools import permutations

log = None


def solve_part_1(puzzle_input):
    checksum_total = 0
    puzzle_input = puzzle_input.replace(' ', '\t')  # Helpful for the examples
    for row in puzzle_input.split('\n'):
        entries = list(int(val) for val in row.split('\t'))
        entries.sort()  # Ints are sorted ascending e.g. [1 (Min), ..., 3 (Max)]
        checksum_row = (entries[-1] - entries[0])  # Checksum is: Max - Min
        log('Row-Checksum: %d' % checksum_row)
        checksum_total += checksum_row
    return checksum_total  # The solution is the total of all checksums


def solve_part_2(puzzle_input):
    checksum_total = 0
    puzzle_input = puzzle_input.replace(' ', '\t')  # Helpful for the examples
    for row in puzzle_input.split('\n'):
        entries = list(int(val) for val in row.split('\t'))
        checksum_row = 0  # Default checksum
        for entry1, entry2 in permutations(entries, 2):
            if entry1 % entry2 is 0:  # Check if entry1 can be devided by entry2
                checksum_row = entry1 // entry2  # <-- The checksum
                break
        else:  # No checksum found
            raise Exception('Could not find any checksum for row: "%s"' % row)
        log('Row-Checksum: %d' % checksum_row)
        checksum_total += checksum_row
    return checksum_total  # The solution is the total of all checksums
