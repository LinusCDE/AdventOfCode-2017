from itertools import count


def solve_part_1(puzzle_input):
    banks_history = list()  # Contains all previous banks as tuples
    banks = list(map(int, puzzle_input.split()))
    total_banks = len(banks)

    for reallocations in count(1):
        biggest_val = max(banks)
        biggest_at = banks.index(biggest_val)

        banks[biggest_at] = 0  # Clear current bank
        # Re-distribute the all blocks on the banks:
        for index in map(lambda index: index % total_banks,  # <- Anti overflow
                         range(biggest_at+1, biggest_at + biggest_val + 1)):
            banks[index] += 1
        banks_tuple = tuple(banks)  # Save new bank allocations as tuple
        if banks_tuple in banks_history:
            return reallocations
        banks_history.append(banks_tuple)


def solve_part_2(puzzle_input):
    pass
