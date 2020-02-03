import re
import sys
from copy import deepcopy
from enum import Enum

from utils.utils import Coordinate as BaseCoordinate


class Type(Enum):
    empty = '.'
    bug = '#'

    @staticmethod
    def from_value(value):
        for elem in [e for e in Type]:
            if elem.value == value:
                return elem

        return None

    def __repr__(self):
        return self.value


def next_state(current_state):
    next_state = deepcopy(current_state)

    for x in range(len(next_state)):
        for y in range(len(next_state[x])):
            bugs = 0
            if x - 1 >= 0:
                up = current_state[x - 1][y]
                if up == Type.bug:
                    bugs += 1

            try:
                down = current_state[x + 1][y]
                if down == Type.bug:
                    bugs += 1
            except IndexError:
                pass

            if y - 1 >= 0:
                left = current_state[x][y - 1]
                if left == Type.bug:
                    bugs += 1

            try:
                right = current_state[x][y + 1]
                if right == Type.bug:
                    bugs += 1
            except IndexError:
                pass

            if current_state[x][y] == Type.bug:
                if bugs == 1:
                    next_state[x][y] = Type.bug
                else:
                    next_state[x][y] = Type.empty

            else:
                if bugs == 1 or bugs == 2:
                    next_state[x][y] = Type.bug
                else:
                    next_state[x][y] = Type.empty

    return next_state


if __name__ == '__main__':
    filename = sys.argv[1]

    with open(filename, 'r') as f:
        content = f.readlines()
        # build map
        current_state = [[None for x in y.strip()] for y in content]

        for i in range(len(current_state)):
            for j in range(len(current_state[i])):
                current_state[i][j] = Type.from_value(content[i][j])

        minutes = 0
        totals = []
        total = 0
        while 1:
            total = 0
            for i in range(len(current_state)):
                for j in range(len(current_state[i])):
                    if current_state[i][j] == Type.bug:
                        total += pow(2, (i*len(current_state[i]) + j))

            if total in totals:
                print(total)
                break
            totals.append(total)
            # print()
            current_state = next_state(current_state)
            minutes += 1

