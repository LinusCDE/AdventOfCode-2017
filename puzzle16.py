
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


def solve_part_1(puzzle_input):
    programs = get_default_order()
    for dance_move in puzzle_input.split(','):
        if dance_move[0] == 's':
            spin(programs, int(dance_move[1:]))
        else:
            a, b = dance_move[1:].split('/')
            if dance_move[0] == 'p':
                partner(programs, a, b)
            elif dance_move[0] == 'x':
                exchange(programs, int(a), int(b))
            else:
                raise Exception('Unexpected dance move: %s' % dance_move)
    return ''.join(programs)


def solve_part_2(puzzle_input):
    pass
