def complex_reverse(elements: list, index: int, length: int):
    size = len(elements)
    first, last = index, index + (length-1)
    first %= size
    last %= size
    for _ in range(length // 2):
        elements[first], elements[last] = elements[last], elements[first]
        first += 1
        last -= 1
        first %= size


def solve_part_1(puzzle_input):
    lengths = map(int, puzzle_input.split(','))
    numbers = list(range(256))
    skip_size = 0
    current_index = 0
    for length in lengths:
        #print(','.join(map(str, numbers)))
        #print(current_index*2*' ' + '-')
        complex_reverse(numbers, current_index, length)
        current_index += length + skip_size
        skip_size += 1
        current_index %= len(numbers)
        skip_size %= len(numbers)
    return numbers[0] * numbers[1]


def ascii_list_of(string: str) -> list:
    return list(map(ord, string))


def xor_of(elements: list) -> int:
    value = 0  # It is save to operate with 0 for the first time
    for element in elements:
        value ^= element
    return value


def safe_hex(number: int) -> str:
    hex_str = hex(number)[2:]
    return ('0' if len(hex_str) is 1 else '') + hex_str


def hash_of(numbers: list) -> str:
    return ''.join(map(safe_hex, numbers))


def solve_part_2(puzzle_input):
    lengths = ascii_list_of(puzzle_input) + [17, 31, 73, 47, 23]
    print(lengths)
    #print('Lengths: %s' % lengths)
    skip_size = 0
    current_index = 0
    numbers = list(range(256))
    for rnd in range(1, 64+1):
        print('Round: %d' % rnd)
        #print('Rnd: %d, Index: %d, Skip: %d' % (rnd, current_index, skip_size))
        len_numbers = len(numbers)
        for length in lengths:
            #print(length)
            complex_reverse(numbers, current_index, length)
            current_index += length + skip_size
            skip_size += 1
            if skip_size >= len_numbers:
                skip_size %= len_numbers
            if current_index >= len_numbers:
                current_index %= len_numbers
            #print(hashlib.md5(str(numbers)).hexdigest())
        #print(current_index, skip_size)
        #print(numbers)
    sparse_hash = []
    for index in map(lambda part: part * 16, range(16)):
        sparse_hash.append(xor_of(numbers[index:index+16]))
    return hash_of(sparse_hash)
