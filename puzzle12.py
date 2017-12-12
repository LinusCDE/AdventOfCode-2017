class Program:

    def __init__(self, identifier: int):
        self.identifier = identifier
        self.communicates_with = list()

    def connect(self, sub_program: 'Program', allow_reconnect=True):
        if sub_program not in self.communicates_with and sub_program is not self:
            self.communicates_with.append(sub_program)
            if allow_reconnect:
                sub_program.connect(self, False)

    def available_programs(self, target: list = [],
                           caller: 'Program'=None) -> list:
        if caller is self:
            return []
        for sub_prog in self.communicates_with:
            if sub_prog not in target:
                target.append(sub_prog)
                sub_prog.available_programs(target, self)
        return target

    def __hash__(self):
        return self.identifier

    def __str__(self):
        return str(self.identifier)

    def __eq__(self, other):
        return str(self) == str(other)

    def __ne__(self, other):
        return not self.__eq__(other)


def get_program(programs: dict, prog_id):
    if prog_id not in programs:
        programs[prog_id] = Program(prog_id)
    return programs[prog_id]


def load_programs(puzzle_input) -> dict:
    programs = {}  # Format {id: Program()}
    for line in puzzle_input.split('\n'):
        sp = line.replace(' <-> ', ', ').split(', ')
        prog_id = int(sp[0])
        other_prog_ids = list(map(int, sp[1:]))
        prog = get_program(programs, prog_id)
        for other_id in other_prog_ids:
            other = get_program(programs, other_id)
            prog.connect(other)
    return programs


def solve_part_1(puzzle_input):
    progs = load_programs(puzzle_input)
    available = progs[0].available_programs()
    return len(available)


def solve_part_2(puzzle_input):
    progs = load_programs(puzzle_input)
    groups = 0
    found_pool = set()  # contains Prog-Ids
    for prog in progs.values():
        if prog in found_pool:
            continue
        groups += 1
        found_pool.add(prog.identifier)
        found_pool.update(map(lambda p: p.identifier, prog.available_programs()))
    return groups
