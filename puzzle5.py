from sys import maxsize


def solve_part_1(puzzle_input):
    jump_list = list(map(int, puzzle_input.split('\n')))  # Input as int-list
    size, current_index = len(jump_list), 0  # Needed variables
    for jump_count in range(1, maxsize):  # Following instructions
        instruction = jump_list[current_index]  # Get the instruction
        jump_list[current_index] += 1  # Change used instruction
        current_index += instruction  # Jump to new index
        if current_index < 0 or current_index >= size:  # Check if in list
            break  # No more in list. Finished
    else:
        raise Exception('Count limit reached!')
    return jump_count


def solve_part_2(puzzle_input):
    jump_list = list(map(int, puzzle_input.split('\n')))
    size, current_index = len(jump_list), 0
    for jump_count in range(1, maxsize):
        instruction = jump_list[current_index]
        # Change to part 1:
        jump_list[current_index] += 1 if instruction < 3 else -1
        # ----------
        current_index += instruction
        if current_index < 0 or current_index >= size:
            break
    else:
        raise Exception('Count limit reached!')
    return jump_count
