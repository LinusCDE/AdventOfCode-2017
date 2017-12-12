class Program:
    '''Representation of a program in the puzzle (day) 12 for AoC 2017.'''

    def __init__(self, identifier: int):
        self.identifier = identifier  # program id
        self.connected = set()  # Direct connections to other Program-instances
        self._hash = identifier  # Value of __hash__() should never change

    def connect(self, other_prog: 'Program', allow_reconnect=True):
        '''Adds 'other_prog' to the list of connected programs for
        this instance as well as the other (beeing be-directional).
        '''
        if other_prog not in self.connected \
           and other_prog is not self:
            self.connected.add(other_prog)
            if allow_reconnect:
                other_prog.connect(self, False)

    def find_reachables(self, target_pool: set = set()) -> set:
        '''Checks for indirect connected programs and puts them into
        'target_pool' which also gets returned for the case, it wasn't
        defined.
        Defining 'target_pool' is used by this method itself to prevent
        inifinite recursion and hence isn't needed to be used.
        '''
        for other_prog in self.connected:
            if other_prog not in target_pool:
                target_pool.add(other_prog)
                other_prog.find_reachables(target_pool)
        return target_pool

    def __hash__(self) -> int:  # To be usable in sets
        return self._hash

    def __eq__(self, other) -> bool:
        '''Is equal when:
        - The Programs are exactly the same instance. E.g:
          - prog1_instance == prog1_instance » True
        - The Programs have an equal identifier. E.g:
          - Program(1) == Program(1) » True
        - The Program has an equal identifier to comparing int. E.g.:
          - Program(6) == 6 » True
        '''
        if self is other:
            return True
        elif isinstance(other, Program):
            return self.identifier == other.identifier
        elif isinstance(other, int):
            return self.identifier == other
        return False


def load_programs(puzzle_input) -> dict:
    '''Load all programs and their direct connections
    from the puzzle input.'''
    programs = {}  # Format {id: Program(id)}

    def get_or_create(prog_id):
        '''Returns the program instance or creates stores and
        returns a new one.
        If the 'prog_'id' is a str. I'll be converted to an int'''
        if isinstance(prog_id, str):  # Is given as an str?
            prog_id = int(prog_id)
        # At this point, 'prog_id' should be an int.
        if prog_id not in programs:
            programs[prog_id] = Program(prog_id)
        return programs[prog_id]

    # Loop through all connections:
    for line in puzzle_input.split('\n'):
        sp = line.replace(' <-> ', ', ').split(', ')
        prog = get_or_create(sp[0])  # Program
        others = map(get_or_create, sp[1:])  # To be connected with
        # Connect to other programs
        for other in others:
            prog.connect(other)
    return programs


def solve_part_1(puzzle_input):
    progs = load_programs(puzzle_input)  # Programs indexed by id
    return len(progs[0].find_reachables())  # All Programs, Prog 0 can reach


def solve_part_2(puzzle_input):
    progs = load_programs(puzzle_input)  # Programs indexed by id
    groups = 0  # Total of different groups found (part 2 solution)
    found_pool = set()  # Found Programs (could contain program ids, too)
    for prog in progs.values():
        # Check if aProgram already belongs to a group:
        if prog.identifier in found_pool:
            continue  # Belongs to a group
        groups += 1  # Doesn't belong to a group, yet

        # Add group to pool of found programs:
        found_pool.add(prog)
        found_pool.update(map(lambda p: p.identifier, prog.find_reachables()))
    return groups
