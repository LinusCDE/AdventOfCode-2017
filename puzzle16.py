
def get_default_order():
    return ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
            'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p']


def spin(programs, amount):
    for _ in range(amount):
        programs.insert(0, programs.pop())


def exchange(programs, a_pos, b_pos):
    a_name, b_name = programs[a_pos], programs[b_pos]
    programs[a_pos] = b_name
    programs[b_pos] = a_name


def partner(programs, a_name, b_name):
    exchange(programs, programs.index(a_name), programs.index(b_name))


def dance(programs, dance_moves):
    for dance_move in dance_moves:
        if dance_move[0] == 's':  # Move with one parameter
            spin(programs, int(dance_move[1:]))
        else:  # Moves with two paramaters
            a, b = dance_move[1:].split('/')
            if dance_move[0] == 'p':
                partner(programs, a, b)
            elif dance_move[0] == 'x':
                exchange(programs, int(a), int(b))
            else:
                raise Exception('Unexpected dance move: %s' % dance_move)


def solve_part_1(puzzle_input):
    programs = get_default_order()
    dance_moves = puzzle_input.split(',')
    dance(programs, dance_moves)
    return ''.join(programs)


def solve_part_2(puzzle_input):
    additional_cycles = 1000000000
    dance_moves = puzzle_input.split(',')
    programs, start_programs = get_default_order(), get_default_order()

    count = 0
    while count < additional_cycles:
        count += 1
        dance(programs, dance_moves)

        if programs == start_programs:
            # Repetition dected. Shortening:
            additional_cycles %= count  # Remaining cycles
            count = 0
    return ''.join(programs)
