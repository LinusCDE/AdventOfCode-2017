def count_valid_phrases(puzzle_input, check_anagrams=False):
    '''Counts the amount of valid phrases'''
    valid = 0
    for phrase in puzzle_input.split('\n'):
        words = []  # Will contain already found words
        for word in phrase.split():
            if check_anagrams:
                word = str().join(sorted(word))  # Sorts all letters alphabetically
            if word in words:
                break  # Word was already found
            words.append(word)
        else:  # No duplicates ((and anagrams)) found
            valid += 1
    return valid


def solve_part_1(puzzle_input):
    return count_valid_phrases(puzzle_input)


def solve_part_2(puzzle_input):
    return count_valid_phrases(puzzle_input, check_anagrams=True)
