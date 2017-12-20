import numpy as np
from itertools import combinations


# Definition of a 'long run'. Probably cheating. But it works. ;D
LONG_RUN_TICKS = 500


class Particle:

    def __init__(self, identifier: int, pos: tuple, vec: tuple, acc: tuple):
        self.identifier = identifier
        self.pos = np.array(pos)
        self.vec = np.array(vec)
        self.acc = np.array(acc)
        self._pos_hash = None

    def __str__(self):
        return 'Particle %d' % self.identifier

    def manhatten_distance_to_zero(self):
        return np.abs(self.pos).sum()

    def tick(self):
        self.vec = np.add(self.vec, self.acc)
        self.pos = np.add(self.pos, self.vec)
        self._pos_hash = None

    def collides(self, other: 'Particle'):
        return self.pos_hash() == other.pos_hash()

    def __hash__(self):
        return self.identifier

    def pos_hash(self):
        if self._pos_hash is None:
            self._pos_hash = hash(str(self.pos))
        return self._pos_hash


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

    # I don't know if its cheating to call 1000 ticks
    # a accurate 'long run'. But it worked for me.
    for tick in range(LONG_RUN_TICKS):

        # Data for collision dectection:
        positions, collided_pos_hashes = set(), set()

        # Update particles and rougly look out for collisions:
        for index, particle in enumerate(particles):
            particle.tick()

            # Used for a rough collision dectection:
            pos_hash = particle.pos_hash()

            # Find collisions
            if pos_hash in positions:
                collided_pos_hashes.add(pos_hash)
            else:
                positions.add(pos_hash)

        # Get particles of collided position hashes:
        collided_particles = set()
        for particle in particles:
            if particle.pos_hash() in collided_pos_hashes:
                collided_particles.add(particle)

        if len(collided_particles) > 0:
            log('Found %d collision(s) during tick %d'
                % (len(collided_particles), tick))

        # Remove collided particles:
        for particle in collided_particles:
            particles.remove(particle)

    return len(particles)
