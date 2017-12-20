from time import time

try:
    import numpy as np
except ImportError:
    print('ERROR: This puzzle (day 20) requires "numpy"!')
    raise RuntimeError()

log = None
# Definition of a 'long run'. Probably cheating. But it works. ;D
LONG_RUN_TICKS = 500


class Particle:
    '''Represents a Particle in the current puzzle (obvious or not?).'''

    def __init__(self, identifier: int, pos: tuple, vec: tuple, acc: tuple):
        self.identifier = identifier
        self.pos = np.array(pos)
        self.vec = np.array(vec)
        self.acc = np.array(acc)
        self._pos_hash_cache = None

    def manhatten_distance_to_zero(self) -> int:
        '''Returns the manhatten distance to zero.'''
        return np.abs(self.pos).sum()

    def tick(self):
        '''Updates the particle according to the puzzle.'''
        self.vec = np.add(self.vec, self.acc)
        self.pos = np.add(self.pos, self.vec)
        self._pos_hash_cache = None  # Clear cache

    def pos_hash(self) -> int:
        '''Returns a simple hash of the current position.
        The hash is cached in '_pos_hash_cache'.
        '''
        if self._pos_hash_cache is None:
            self._pos_hash_cache = hash(str(self.pos))
        return self._pos_hash_cache


def load_particles(puzzle_input) -> list:
    particles = []

    for identifier, line in enumerate(puzzle_input.split('\n')):
        data = line.split(', ')
        for i in range(len(data)):
            data[i] = data[i][3:-1]  # Strip off 'X=<' and '>'

        pos = tuple(map(int, data[0].split(',')))
        vec = tuple(map(int, data[1].split(',')))
        acc = tuple(map(int, data[2].split(',')))

        particles.append(Particle(identifier, pos, vec, acc))

    return particles


def solve_part_1(puzzle_input):
    particles = load_particles(puzzle_input)

    for _ in range(LONG_RUN_TICKS):
        for particle in particles:
            particle.tick()

    nearest = min(particles,
                  key=lambda particle: particle.manhatten_distance_to_zero())
    return nearest.identifier


def solve_part_2(puzzle_input):
    particles = load_particles(puzzle_input)

    last_progress_report = time()

    for tick in range(LONG_RUN_TICKS):

        # ----- Report progress: -----
        if time() - last_progress_report > 1.5:
            last_progress_report = time()
            print('Progress: %d%%' % ((tick + 1) * 100 / LONG_RUN_TICKS))

        # ---- Update particles and look out for collisions: ----
        pos_hashes, collided_pos_hashes = set(), set()
        for particle in particles:
            particle.tick()

            pos_hash = particle.pos_hash()  # Used for collision dectection

            # Find collisions
            if pos_hash not in pos_hashes:
                pos_hashes.add(pos_hash)
            else:
                collided_pos_hashes.add(pos_hash)

        # ----- Resolve and remove collided particles: ------
        if len(collided_pos_hashes) > 0:
            collisions = 0

            for particle in tuple(particles):  # (mutation during iteration)
                if particle.pos_hash() in collided_pos_hashes:
                    particles.remove(particle)
                    collisions += 1

            log('Tick %d: Removed %d collided particles.' % (tick, collisions))

    return len(particles)
