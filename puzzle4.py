log = None


POLICY_NO_DUPLICATES = 0
POLICY_NO_ANAGRAMS = 1


def valid(phrase, policies):
    words = []
    for word in phrase.split(' '):
        if POLICY_NO_ANAGRAMS in policies:
            word = list(word)
            word.sort()
            word = str().join(word)
        if word in words and POLICY_NO_DUPLICATES in policies:
            return False
        words.append(word)
    return True


def count(puzzle_input, policies):
    valid_count = 0
    for phrase in puzzle_input.split('\n'):
        if valid(phrase, policies):
            valid_count += 1
    return valid_count


def solve_part_1(puzzle_input):
    return count(puzzle_input, [POLICY_NO_DUPLICATES])



def solve_part_2(puzzle_input):
    return count(puzzle_input, [POLICY_NO_DUPLICATES, POLICY_NO_ANAGRAMS])

