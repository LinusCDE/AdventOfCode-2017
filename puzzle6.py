from itertools import count


print('Hint: Run this puzzle with \'pypy3\' to get improved performance')


def find_duplicate_allocation(banks: str) -> tuple:
    '''Returns the reallocation count as well as the index of the duplicated
     bank that was found.'''
    banks_history = list()  # Contains all previous banks as checksums
    banks = list(map(int, banks.split()))
    total_banks = len(banks)

    for reallocations in count(1):
        biggest_val, biggest_at = 0, 0
        for index, val in enumerate(banks):
            if val > biggest_val:
                biggest_val = val
                biggest_at = index

        banks[biggest_at] = 0  # Clear current bank
        # Re-distribute the all blocks on the banks:
        for index in range(biggest_at + 1, biggest_at + biggest_val + 1):
            banks[index % total_banks] += 1

        # Checksum of the current bank for faster finding in banks_history:
        checksum = ','.join(map(str, banks))

        if checksum in banks_history:
            seen_at = banks_history.index(checksum)
            return (reallocations, seen_at + 1)
        banks_history.append(checksum)


def solve_part_1(puzzle_input):
    return find_duplicate_allocation(puzzle_input)[0]


def solve_part_2(puzzle_input):
    result = find_duplicate_allocation(puzzle_input)
    return result[0] - result[1]
