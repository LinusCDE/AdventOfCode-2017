def spin(value_count=2018, steps=3) -> tuple:
    buffer, index, last_inserted = [0], 0, 0
    for _ in range(value_count - 1):
        index += steps
        index %= len(buffer)
        last_inserted += 1
        buffer.insert(index + 1, last_inserted)
        index += 1
    return buffer, index


def solve_part_1(puzzle_input):
    buffer, index = spin(steps=int(puzzle_input))
    return buffer[(index + 1) % len(buffer)]


def solve_part_2(puzzle_input):
    pass
