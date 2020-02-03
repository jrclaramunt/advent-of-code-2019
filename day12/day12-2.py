import itertools
import re
import sys

from utils.utils import Coordinate as BaseCoordinate


class Coordinate3D(BaseCoordinate):

    def __init__(self, x, y, z):
        super().__init__(x, y)
        self.z = z

    def __str__(self):
        return f'{super().__str__()}, z: {self.z}'

    def __eq__(self, other):
        return super().__eq__(other) and other.z == self.z


class Speed(Coordinate3D):
    pass


class Moon:
    def __init__(self, coordinate):
        self.position = coordinate
        self.speed = Speed(0, 0, 0)

    def update_speed(self, moon):
        if self.position.x > moon.position.x:
            self.speed.x -= 1

        elif self.position.x < moon.position.x:
            self.speed.x += 1

        if self.position.y > moon.position.y:
            self.speed.y -= 1

        elif self.position.y < moon.position.y:
            self.speed.y += 1

        if self.position.z > moon.position.z:
            self.speed.z -= 1

        elif self.position.z < moon.position.z:
            self.speed.z += 1

    def update_position(self):
        self.position.x += self.speed.x
        self.position.y += self.speed.y
        self.position.z += self.speed.z

    def potential(self):
        return abs(self.position.x) + abs(self.position.y) + abs(self.position.z)

    def kinetic(self):
        return abs(self.speed.x) + abs(self.speed.y) + abs(self.speed.z)

    def __eq__(self, other):
        return self.position == other.position and self.speed == other.speed


if __name__ == '__main__':
    filename = sys.argv[1]

    regex = '^<x=(-*\d+), y=(-*\d+), z=(-*\d+)>$'
    moons = []
    steps = 1000

    with open(filename, 'r') as f:
        content = f.readlines()

        for line in content:
            parsed_line = re.search(regex, line).groups()
            coordinate = Coordinate3D(x=int(parsed_line[0]), y=int(parsed_line[1]), z=int(parsed_line[2]))
            moon = Moon(coordinate)
            moons.append(moon)

    for _ in range(steps):
        for i in range(len(moons)):
            for j in range(len(moons)):
                if j != i:
                    moons[i].update_speed(moons[j])

        for moon in moons:
            moon.update_position()

    total = 0
    for moon in moons:
        total += moon.potential() * moon.kinetic()

    print(total)

    moons2 = []
    for line in content:
        parsed_line = re.search(regex, line).groups()
        coordinate = Coordinate3D(x=int(parsed_line[0]), y=int(parsed_line[1]), z=int(parsed_line[2]))
        moon = Moon(coordinate)
        moons2.append(moon)

    initial = []
    for line in content:
        parsed_line = re.search(regex, line).groups()
        coordinate = Coordinate3D(x=int(parsed_line[0]), y=int(parsed_line[1]), z=int(parsed_line[2]))
        moon = Moon(coordinate)
        initial.append(moon)

    step = 0
    a = 0
    while(1):
        for i in range(len(moons2)):
            for j in range(len(moons2)):
                if j != i:
                    moons2[i].update_speed(moons2[j])

        for i in range(len(moons2)):
            moons2[i].update_position()

        if moons2[0].position == initial[0].position:
            print(f'index {0} step {step}')
        # print(moons2[0].position.x)
        step += 1





