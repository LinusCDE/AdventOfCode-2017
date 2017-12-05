def solve_part_1(puzzle_input):
    jump_list = list(map(int, puzzle_input.split('\n')))  # Input as int-list
    size, current_index, jump_count = len(jump_list), 0, 0  # Needed variables
    while True:  # Following instructions
        instruction = jump_list[current_index]  # Get the instruction
        jump_list[current_index] += 1  # Change used instruction
        current_index += instruction  # Jump to new index
        jump_count += 1  # Step counting
        if current_index < 0 or current_index >= size:  # Check if in list
            break  # No more in list. Finished
    return jump_count


def solve_part_2(puzzle_input):
    jump_list = list(map(int, puzzle_input.split('\n')))
    size, current_index, jump_count = len(jump_list), 0, 0
    while True:
        instruction = jump_list[current_index]
        # Change to part 1:
        jump_list[current_index] += 1 if instruction < 3 else -1
        # ----------
        current_index += instruction
        jump_count += 1
        if current_index < 0 or current_index >= size:
            break
    return jump_count
