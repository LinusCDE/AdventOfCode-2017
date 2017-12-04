log = None


POLICY_NO_DUPLICATES = 0
POLICY_NO_ANAGRAMS = 1


def phrase_valid(phrase, policies):
    '''Ckecks if the given phrase satisfies all given policies'''
    words = []  # Will contain already found words
    for word in phrase.split(' '):
        if POLICY_NO_ANAGRAMS in policies:
            word = str().join(sorted(word))  # Sorts all letters alphabetically
        if word in words and POLICY_NO_DUPLICATES in policies:
            return False  # Word was already found
        words.append(word)
    return True


def count_valid_phrases(puzzle_input, policies):
    '''Counts the amount of valid phrases'''
    valid = 0
    for phrase in puzzle_input.split('\n'):
        if phrase_valid(phrase, policies):
            valid += 1
    return valid


def solve_part_1(puzzle_input):
    return count_valid_phrases(puzzle_input, [POLICY_NO_DUPLICATES])



def solve_part_2(puzzle_input):
    return count_valid_phrases(puzzle_input, [POLICY_NO_DUPLICATES, POLICY_NO_ANAGRAMS])

