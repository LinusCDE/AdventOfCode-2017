def complex_reverse(elements: list, index: int, length: int):
    '''Reverses a specified sub-list in 'elements'.'''
    size = len(elements)  # To save some computation time
    first, last = index, (index + (length-1)) % size
    for _ in range(length // 2):
        # Swap first and last elements:
        elements[first], elements[last] = elements[last], elements[first]
        first = (first + 1) % size  # Forward one step
        last -= 1  # Negative numbers (such as -1, -2) are fine in python


def gen_knot(lengths: list, rounds: int = 1):
    '''Generates the knot with given 'lenghts' and 'rounds'.'''
    knot = list(range(256))  # List to be processed
    knot_size = len(knot)  # Just to be safe. Will be 256
    skip, cursor = 0, 0
    for _ in range(rounds):
        for length in lengths:
            complex_reverse(knot, cursor, length)
            cursor += length + skip
            skip += 1
            # Prevent unneccessary slowdown in part 2:
            cursor, skip = cursor % knot_size, skip % knot_size
    return knot


def solve_part_1(puzzle_input):
    lengths = map(int, puzzle_input.split(','))
    knot = gen_knot(lengths)
    return knot[0] * knot[1]


def ascii_codes(string: str) -> list:
    '''Returns the ascii-codes of each character as list.'''
    return list(map(ord, string))


def xor_all(elements: list) -> int:
    '''Returns the combined xor-result of each element in the list 'elements'
    Note that 'elements' is expected to be filled only with ints.
    '''
    value = 0  # It is save to operate with 0 for the first time
    for element in elements:
        value ^= element  # Xor with last xor-result
    return value


def safe_hex(number: int) -> str:
    '''Adds a leading 0 and removes the '0x'-prefix from the hex()-function.'''
    hex_str = hex(number)[2:]
    return ('0' if len(hex_str) is 1 else '') + hex_str


def solve_part_2(puzzle_input):
    # Get lengths as accii-codes and append the given suffix:
    lengths = ascii_codes(puzzle_input) + [17, 31, 73, 47, 23]
    knot = gen_knot(lengths, rounds=64)
    # Generates the dense hash:
    dense_hash = [xor_all(knot[index:index+16])
                  for index in map(lambda part: part * 16, range(16))]
    # Hex all values of the dense hash together:
    return ''.join(map(safe_hex, dense_hash))
