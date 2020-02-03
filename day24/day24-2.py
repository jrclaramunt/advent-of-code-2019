import re
import sys
from copy import deepcopy
from enum import Enum

from utils.utils import Coordinate as BaseCoordinate


class Type(Enum):
    empty = '.'
    bug = '#'
    eris = '?'

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


def init_state():
    return [[Type.empty] * 5] * 5


def next_state_inner(current_state, outer_state):
    next_state = deepcopy(current_state)

    for x in range(len(next_state)):
        for y in range(len(next_state[x])):
            bugs = 0
            if x - 1 >= 0:
                up = current_state[x - 1][y]
            else:
                up = outer_state[1][2]

            if up == Type.bug:
                bugs += 1

            try:
                down = current_state[x + 1][y]
            except IndexError:
                down = outer_state[3][2]

            if down == Type.bug:
                bugs += 1

            if y - 1 >= 0:
                left = current_state[x][y - 1]
            else:
                left = outer_state[2][1]

            if left == Type.bug:
                bugs += 1

            try:
                right = current_state[x][y + 1]
            except IndexError:
                right = outer_state[2][3]

            if right == Type.bug:
                bugs += 1

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


def next_state_2(current_state, inner_state, outer_state):
    next_state = deepcopy(current_state)

    for x in range(len(next_state)):
        for y in range(len(next_state[x])):
            bugs = 0
            if x - 1 >= 0:
                if x == 3 and y == 2:
                    for z in range(5):
                        if inner_state[4][z] == Type.bug:
                            bugs += 1
                else:
                    up = current_state[x - 1][y]
                    if up == Type.bug:
                        bugs += 1
            else:
                up = outer_state[1][2]
                if up == Type.bug:
                    bugs += 1

            try:
                if x == 1 and y == 2:
                    for z in range(5):
                        if inner_state[0][z] == Type.bug:
                            bugs += 1
                else:
                    down = current_state[x + 1][y]
                    if down == Type.bug:
                        bugs += 1
            except IndexError:
                down = outer_state[3][2]
                if down == Type.bug:
                    bugs += 1

            if y - 1 >= 0:
                if x == 2 and y == 3:
                    for z in range(5):
                        if inner_state[z][4] == Type.bug:
                            bugs += 1
                else:
                    left = current_state[x][y - 1]
                    if left == Type.bug:
                        bugs += 1
            else:
                left = outer_state[2][1]
                if left == Type.bug:
                    bugs += 1

            try:
                if x == 1 and y == 2:
                    for z in range(5):
                        if inner_state[z][0] == Type.bug:
                            bugs += 1
                else:
                    right = current_state[x][y + 1]
                    if right == Type.bug:
                        bugs += 1
            except IndexError:
                right = outer_state[2][3]
                if right == Type.bug:
                    bugs += 1

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
        initial_state = deepcopy(current_state)

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

        initial_state[2][2] = Type.eris

        minutes = 10
        result = {}

        result[0] = initial_state

        for level in range(minutes):
            next_state_2(current_level_state, inner_state)
            for i in range(0, level + 1):
                inner_state_index = i
                outer_state_index = -i



                inner_state = result[i - 1]
                try:
                    current_level_state = result[i]
                except KeyError:
                    current_level_state = init_state()

                try:
                    current_level_state = result[i]
                except KeyError:
                    current_level_state = init_state()

                result[negative_index] = next_state_2(current_level_state, inner_state)




