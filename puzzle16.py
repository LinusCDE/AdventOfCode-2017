# First oder of the programs. This shall not be mutated (therefore as a tuple):
PROGAMS_START = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p')


def do_spin(programs, amount):
    '''Performs the spin move on 'programs' using 'amount'.'''
    for _ in range(amount):
        programs.insert(0, programs.pop())


def do_exchange(programs, a_pos, b_pos):
    '''Performs the exchange move on 'programs' using 'a_pos' and 'b_pos'.'''
    programs[a_pos], programs[b_pos] = programs[b_pos], programs[a_pos]


def do_partner(programs, a_name, b_name):
    '''Performs the partner move on 'programs' using 'a_name' and 'b_name'.'''
    do_exchange(programs, programs.index(a_name), programs.index(b_name))


def parse_dance_functions(puzzle_input) -> list:
    '''Returns a list with all functions that requiere the 'programs'-list,
    but already have the parsed parameters.
    Used to prevent parsing the 'puzzle_input' over and over again in part 2.
    '''
    dance_functions = list()  # Contains lambdas that take 'programs' as 1st arg

    for dance_move in puzzle_input.split(','):
        function = None
        if dance_move[0] == 's':  # Move with one parameter
            function = (lambda progs, amount=int(dance_move[1:]):
                        do_spin(progs, amount))
        else:  # Moves with two paramaters
            a, b = dance_move[1:].split('/')  # Get the two dance parameters

            if dance_move[0] == 'p':
                function = (lambda progs, a=a, b=b: do_partner(progs, a, b))
            elif dance_move[0] == 'x':
                a, b = map(int, (a, b))
                function = (lambda progs, a=a, b=b: do_exchange(progs, a, b))

        dance_functions.append(function)
    return dance_functions


# Cache dances to improve performance in part 2
# Format: {'programs_hash1' (int): result_programs1 (list), ...}
dance_cache = dict()


def dance(input_programs, dance_functions) -> list:
    '''Perform one dance with 'dance_functions' and 'input_programs'.
    Returning new order. 'input_programs' will not be modified.
    '''
    # Check cache:
    global dance_cache
    input_programs_hash = hash(''.join(input_programs))

    if input_programs_hash in dance_cache:
        return dance_cache[input_programs_hash]

    # Peform dance. Invoking all dance_functions on 'programs':
    programs = list(input_programs)
    for dance_function in dance_functions:
        dance_function(programs)

    # Store output in cache:
    dance_cache[input_programs_hash] = programs
    return programs


def solve_part_1(puzzle_input):
    # Get programs and dance moves:
    programs = list(PROGAMS_START)
    dance_functions = parse_dance_functions(puzzle_input)

    programs = dance(programs, dance_functions)

    return ''.join(programs)


def solve_part_2(puzzle_input):
    dance_functions = parse_dance_functions(puzzle_input)
    programs, start_programs = list(PROGAMS_START), list(PROGAMS_START)

    count = 0
    total_cycles = int(10e8)  # '10e8' (= 1 billion) would output a float

    while count < total_cycles:  # total_cycles will be changed later on
        count += 1
        programs = dance(programs, dance_functions)

        if programs == start_programs:
            # Repetition dected. Shortening:
            total_cycles %= count  # Remaining cycles
            count = 0

    return ''.join(programs)
