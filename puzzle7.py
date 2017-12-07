'''
Help for part 2:
https://gist.github.com/LinusCDE/109536a4a4b319c107c6112b6efb89d9
'''


log = None


def parse_data(puzzle_input: str) -> tuple:
    '''Extracts all data from puzzle_input.

    Returns a tuple which contains two lists:
    - The first ('held_data') has all information for which tower/program bears
    which other towers (non-recursive!).
    - The second dicts contains the weight of each tower but NOT the sub-towers.
    '''
    weight_data = {}  # Format: {tower1, weight1, tower2: weight2, ...}
    held_data = {}  # Format: {tower1: [progtower2, tower3, ...], ...}
    for line in puzzle_input.split('\n'):
        tower_name, holding = None, []
        if ' -> ' in line:
            line = line.split(' -> ')
            tower_name = line[0]
            holding = line[1].split(', ') if ', ' in line[1] else [line[1]]
        else:
            tower_name = line.strip()
        splitted = tower_name.split(' (')
        tower_name = splitted[0]
        held_data[tower_name] = holding
        weight_data[tower_name] = int(splitted[1][:-1])
    return held_data, weight_data


def root_tower_name(held_data: dict) -> str:
    possibles = list(held_data.keys())
    for holding in held_data.values():
        for tower in holding:
            possibles.remove(tower)
    if len(possibles) is not 1:
        raise Exception('Failed to find root-tower!')
    return possibles[0]


def solve_part_1(puzzle_input):
    held_data = parse_data(puzzle_input)[0]
    return root_tower_name(held_data)


def minority(elms) -> int:
    '''Finds the minority and returns the index of its first occurrence.
    If there is no miority, 'None' will be returned.
    '''
    if len(elms) is 0:
        return None
    elm_count = {}  # Format: {value: count}
    for elm in elms:
        elm_count[elm] = elm_count.get(elm, 0) + 1
    last_count = None
    for count in elm_count.values():
        if last_count is None:
            last_count = count
        if count != last_count:
            break
    else:
        return None  # No minority available
    # Return the index of the element whose value was found least often:
    return elms.index(min(elms, key=lambda elm: elm_count[elm]))


class Tower:
    '''Representation of the Towers in the puzzle. For easier understanding
    the towers have the names of the programs supporting them.
    '''

    def __init__(self, name: str, weight: int,
                 parent: 'Tower'=None, sub_towers=[]):
        self.name = name
        self.weight = weight
        self.parent = parent  # <- For the root tower this will be: None
        self.sub_towers = sub_towers  # <- The towers 'on the disk'
        self.__total_weight_cached = None

        if parent is not None:
            parent.__total_weight_cached = None

    def total_weight(self) -> int:
        '''Returns the total weight bearing on this tower
        (own weight + weight of all sub-towers and their sub-towers, ...)
        '''
        # Compute value if not cached:
        if self.__total_weight_cached is None:
            sub_towers_weight = sum(map(lambda tower: tower.total_weight(),
                                        self.sub_towers))
            self.__total_weight_cached = self.weight + sub_towers_weight
        return self.__total_weight_cached

    def find_unbalanced_tower(self, default=None) -> 'Tower':
        '''Returns either a unbalanced sub-sub-...-tower or default.'''
        sub_towers = self.sub_towers
        # Generate tuple of the total weight of all sub towers
        sub_towers_weight = tuple(map(lambda t: t.total_weight(), sub_towers))
        index = minority(sub_towers_weight)
        if index is None:
            return default  # No faults in the sub-towers

        suspect = sub_towers[index]
        # Either the tower (suspect) says that the misbalance is someone
        # elses fault or he is it himself:
        unbalanced = suspect.find_unbalanced_tower(default=suspect)
        return unbalanced

    def __str__(self):
        return '%s (%d)' % (self.name, self.weight)


def data_to_tower(name: str, held_data: dict,
                  weight_data: dict, parent: Tower=None) -> Tower:
    '''Gets a Tower by name with all sub-towers assigned recursivly.'''
    if name not in held_data:  # No sub-towers available
        return Tower(name, weight_data[name], parent=parent)

    sub_towers = []
    tower = Tower(name, weight_data[name], sub_towers=sub_towers, parent=parent)

    for sub_tower in held_data[name]:
        sub_towers.append(data_to_tower(sub_tower, held_data,
                                        weight_data, parent=tower))

    return tower


def solve_part_2(puzzle_input):
    held_data, weight_data = parse_data(puzzle_input)  # Data parsed as lists

    tower_root_name = root_tower_name(held_data)  # Name of the root-tower
    tower_root = data_to_tower(tower_root_name, held_data, weight_data)

    misbalanced = tower_root.find_unbalanced_tower()  # <- HE IS IT!
    if misbalanced is None:
        raise Exception('Failed to find the misbalanced tower!')

    # Find correct weight of the tower 'misbalanced':
    expected_total_weight = None
    for neighbor in misbalanced.parent.sub_towers:
        if neighbor.total_weight() != misbalanced.total_weight():
            expected_total_weight = neighbor.total_weight()
            break
    else:
        raise Exception('Failed to get the expected weight.')

    # Weight of all the stuff the tower 'misplaced' is carrying:
    sub_weight = misbalanced.total_weight() - misbalanced.weight
    # The correct weight is the expected weight (total) minus the 'sub_weight':
    correct_weight = expected_total_weight - sub_weight
    log('Tower/Program with the wrong weight: %s' % misbalanced)
    return correct_weight
