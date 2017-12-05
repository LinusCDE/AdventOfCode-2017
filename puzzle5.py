def solve_part_1(puzzle_input):
    jump_list = list(map(int, puzzle_input.split('\n')))
    size, current_index, jump_count = len(jump_list), 0, 0
    while True:
        index, instruction = current_index, jump_list[current_index]
        current_index += instruction
        jump_list[index] += 1
        jump_count += 1
        if current_index < 0 or current_index >= size:
            break
    return jump_count


def solve_part_2(puzzle_input):
    jump_list = list(map(int, puzzle_input.split('\n')))
    size, current_index, jump_count = len(jump_list), 0, 0
    while True:
        index, instruction = current_index, jump_list[current_index]
        current_index += instruction
        jump_list[index] += 1 if instruction < 3 else -1
        jump_count += 1
        if current_index < 0 or current_index >= size:
            break
    return jump_count
