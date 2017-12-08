log = None


def execute(line: str, register: dict):
    split = line.split()
    do_name, do_action, do_value, _, when_name, when_action, when_value = split
    if len(when_action) > 2:
        raise Exception('Security Breach! (%s)' % when_action)
    if when_name not in register:
        register[when_name] = 0
    if(eval('register[\'%s\'] %s %s' % (when_name, when_action, when_value))):
        do_value = int(do_value)
        if do_action == 'dec':
            do_value *= -1
        register[do_name] = ret = register.get(do_name, 0) + do_value
        return ret
    return 0


def solve_part_1(puzzle_input):
    register = {}
    for line in puzzle_input.split('\n'):
        execute(line, register)
    log(register)
    return max(register.values())


def solve_part_2(puzzle_input):
    register, highest = {}, 0
    for line in puzzle_input.split('\n'):
        highest = max(execute(line, register), highest)
    log(register)
    return highest
