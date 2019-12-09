import sys
from collections import defaultdict
from enum import Enum

from utils.utils import Coordinate as BaseCoordinate


class Coordinate(BaseCoordinate):
    def __init__(self, x, y, steps=0):
        super().__init__(x, y)
        self.steps = steps


class Direction(Enum):
    Up = 'U'
    Right = 'R'
    Down = 'D'
    Left = 'L'


class Panel:
    def __init__(self, central_port):
        self.central_port = central_port
        self.coordinates_map = defaultdict(set)

    def create_coordinates_map(self, wires):

        current_coordinate = self.central_port
        steps = 0
        for wire in wires:

            direction = wire[0]
            fragments = int(wire[1:])

            for i in range(1, fragments + 1):
                steps += 1
                if direction == Direction.Up.value:
                    c = Coordinate(current_coordinate.x - i, current_coordinate.y, steps)
                if direction == Direction.Right.value:
                    c = Coordinate(current_coordinate.x, current_coordinate.y + i, steps)
                if direction == Direction.Down.value:
                    c = Coordinate(current_coordinate.x + i, current_coordinate.y, steps)
                if direction == Direction.Left.value:
                    c = Coordinate(current_coordinate.x, current_coordinate.y - i, steps)

                self.coordinates_map[c.x].add(c)

            current_coordinate = c

    def intersections(self, wires):
        current_coordinate = self.central_port
        intersections_found = set()
        steps = 0

        for wire in wires:

            direction = wire[0]
            fragments = int(wire[1:])

            for i in range(1, fragments + 1):
                steps += 1
                if direction == Direction.Up.value:
                    c = Coordinate(current_coordinate.x - i, current_coordinate.y, steps)
                if direction == Direction.Right.value:
                    c = Coordinate(current_coordinate.x, current_coordinate.y + i, steps)
                if direction == Direction.Down.value:
                    c = Coordinate(current_coordinate.x + i, current_coordinate.y, steps)
                if direction == Direction.Left.value:
                    c = Coordinate(current_coordinate.x, current_coordinate.y - i, steps)

                try:
                    coordinates = self.coordinates_map[c.x].copy()
                    self.coordinates_map[c.x].remove(c)
                    intersection = self.coordinates_map[c.x] ^ coordinates
                    c.steps += intersection.pop().steps
                    intersections_found.add(c)
                except KeyError:
                    continue

            current_coordinate = c

        return intersections_found


if __name__ == '__main__':
    filename = sys.argv[1]

    with open(filename, 'r') as f:
        input = f.readlines()

        wires1 = list(input[0].split(","))
        wires2 = list(input[1].split(","))

        central_port = Coordinate(0, 0)

        panel = Panel(central_port)
        panel.create_coordinates_map(wires1)
        intersections = panel.intersections(wires2)

        lowest_manhattan_distance = sys.maxsize
        lowest_amount_of_steps = sys.maxsize

        for intersection in list(intersections):
            if intersection.manhattan_distance(central_port) <= lowest_manhattan_distance:
                lowest_manhattan_distance = intersection.manhattan_distance(central_port)

            if intersection.steps <= lowest_amount_of_steps:
                lowest_amount_of_steps = intersection.steps

        print(f'Lowest manhattan distance: {lowest_manhattan_distance}')
        print(f'Lowest amount of steps: {lowest_amount_of_steps}')
