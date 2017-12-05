def solve_part_1(puzzle_input):
    jump_list = list(map(int, puzzle_input.split('\n')))
    current_index = 0
    jump_count = 0
    while current_index >= 0 and current_index < len(jump_list):
        index = current_index
        current_index += jump_list[current_index]
        jump_list[index] += 1
        jump_count += 1
    return jump_count


def solve_part_2(puzzle_input):
    jump_list = list(map(int, puzzle_input.split('\n')))
    current_index = 0
    jump_count = 0
    while current_index >= 0 and current_index < len(jump_list):
        index = current_index
        current_index += jump_list[current_index]
        jump_list[index] += 1 if jump_list[index] < 3 else -1
        jump_count += 1
    return jump_count
