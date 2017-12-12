class Program:

    def __init__(self, identifier: int, communicates_with: list = []):
        self.identifier = identifier
        self.communicates_with = communicates_with

    def available_programs(self, target: set):
        if self in target:
            return
        for prog in self.communicates_with:
            if prog not in target:
                target.update(target)
                prog.available_programs(target)


def load_programs(puzzle_input) -> dict:
    programs = {}  # Format {id: Program()}
    for line in puzzle_input.split('\n'):
        sp = line.replace(' <-> ', ', ').split(', ')
        prog_id = int(sp[0])
        other_prog_ids = list(map(int, sp[1:]))
        prog_class = programs[prog_id] = Program(prog_id)
        for other_prog_id in other_prog_ids:
            if other_prog_id in programs:
                programs[other_prog_id].communicates_with.append(prog_class)
            else:
                programs[other_prog_id] = Program(other_prog_id, [prog_class])
            prog_class.communicates_with.append(programs[other_prog_id])
    return programs


def solve_part_1(puzzle_input):
    progs = load_programs(puzzle_input)
    log('Searching...')
    available = set()
    progs[0].available_programs(available)
    return len(list(available)) - 1


def solve_part_2(puzzle_input):
    pass
