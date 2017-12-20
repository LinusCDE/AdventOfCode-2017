import numpy as np


class Particle:

    def __init__(self, identifier: int, pos: tuple, vec: tuple, acc: tuple):
        self.identifier = identifier
        self.pos = np.array(pos)
        self.vec = np.array(vec)
        self.acc = np.array(acc)

    def __str__(self):
        return 'Particle %d' % self.identifier

    def manhatten_distance_to_zero(self):
        return np.abs(self.pos).sum()

    def tick(self):
        self.vec = np.add(self.vec, self.acc)
        self.pos = np.add(self.pos, self.vec)


def load_particles(puzzle_input) -> list:
    particles = []

    for identifier, line in enumerate(puzzle_input.split('\n')):
        data = line.split(', ')
        for i in range(len(data)):
            data[i] = data[i][3:-1]  # Strip of X=<DATA>

        pos = tuple(map(int, data[0].split(',')))
        vec = tuple(map(int, data[1].split(',')))
        acc = tuple(map(int, data[2].split(',')))

        particles.append(Particle(identifier, pos, vec, acc))

    return particles


def solve_part_1(puzzle_input):
    particles = load_particles(puzzle_input)

    # I don't know if its cheating to call 1000 ticks
    # a accurate 'long run'. But it worked for me.
    for _ in range(1000):
        for particle in particles:
            particle.tick()

    nearest = min(particles,
                  key=lambda particle: particle.manhatten_distance_to_zero())
    return nearest.identifier


def solve_part_2(puzzle_input):
    pass
