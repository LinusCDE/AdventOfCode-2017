from itertools import count


def find_duplicate_allocation(banks: str):
    '''Returns the reallocation count as well as the index of the duplicated
     bank that was found.'''
    banks_history = list()  # Contains all previous banks as tuples
    banks = list(map(int, banks.split()))
    total_banks = len(banks)

    for reallocations in count(1):
        biggest_val = max(banks)
        biggest_at = banks.index(biggest_val)

        banks[biggest_at] = 0  # Clear current bank
        # Re-distribute the all blocks on the banks:
        for index in map(lambda index: index % total_banks,  # prevent overflow
                         range(biggest_at+1, biggest_at + biggest_val + 1)):
            banks[index] += 1
        banks_tuple = tuple(banks)  # Save new bank allocations as tuple
        if banks_tuple in banks_history:
            seen_at = banks_history.index(banks_tuple)
            return (reallocations, seen_at + 1)
        banks_history.append(banks_tuple)


def solve_part_1(puzzle_input):
    return find_duplicate_allocation(puzzle_input)[0]


def solve_part_2(puzzle_input):
    result = find_duplicate_allocation(puzzle_input)
    return result[0] - result[1]
