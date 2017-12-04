log = None


def valid(phrase):
    words = []
    for word in phrase.split(' '):
        if word in words:
            return False
        words.append(word)
    return True

def solve_part_1(puzzle_input):
    valid_count = 0
    for phrase in puzzle_input.split('\n'):
        if valid(phrase):
            valid_count += 1
    return valid_count

def solve_part_2(puzzle_input):
    pass
