def spin(value_count=2018, steps=3) -> tuple:
    buffer, index = [0], 0
    for inserting in range(1, value_count):
        index = ((index + steps) % inserting) + 1
        buffer.insert(index, inserting)
        print(buffer.index(1))
    return buffer, index


def solve_part_1(puzzle_input):
    buffer, index = spin(steps=int(puzzle_input))
    print(buffer)
    return buffer[(index + 1) % len(buffer)]


def solve_part_2(puzzle_input):
    index = 0
    final = -1
    steps = int(puzzle_input)
    for inserting in range(1, 50000000):
        index = ((index + steps) % inserting) + 1
        if index == 1:
            final = inserting
    return final
