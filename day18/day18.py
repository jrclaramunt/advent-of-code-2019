import re
import sys
from enum import Enum

from utils.utils import Coordinate as BaseCoordinate


class Type(Enum):
    entrance = '@'
    open_passage = '.'
    stone_wall = '#'
    key = 'k'
    door = 'd'

    @staticmethod
    def from_value(value):
        if re.findall('[a-z]', value):
            return Type.key
        if re.findall('[A-Z]', value):
            return Type.door

        for elem in [e for e in Type]:
            if elem.value == value:
                return elem

        return None


class Node(BaseCoordinate):

    def __init__(self, x, y, type, data=None, parent=None, g=0, h=0):
        super().__init__(x, y)
        self.type = type
        self.data = data
        self.parent = parent
        self.g = g
        self.h = h
        self.f = self.g + self.h

    def update_f(self):
        self.f = self.g + self.h

    def __str__(self):
        if self.data is None:
            return f'{self.type.value} -> ({self.x},{self.y})'
        else:
            return f'{self.type.value}:{self.data} -> ({self.x},{self.y})'

    def __repr__(self):
        return f'{self.type.value}'


def get_node_successors(node, vault_map, keys):
    node_successors = []
    try:
        up = vault_map[node.x - 1][node.y]
        if up.type != Type.stone_wall:
            if up.type == Type.door and up.data.lower() in keys:
                node_successors.append(up)
            if up.type != Type.door:
                node_successors.append(up)
    except IndexError:
        pass

    try:
        down = vault_map[node.x + 1][node.y]
        if down.type != Type.stone_wall:  # and down.type != Type.door:
            if down.type == Type.door and down.data.lower() in keys:
                node_successors.append(down)
            if down.type != Type.door:
                node_successors.append(down)
    except IndexError:
        pass

    try:
        left = vault_map[node.x][node.y - 1]
        if left.type != Type.stone_wall:  # and left.type != Type.door:
            if left.type == Type.door and left.data.lower() in keys:
                node_successors.append(left)
            if left.type != Type.door:
                node_successors.append(left)
    except IndexError:
        pass

    try:
        right = vault_map[node.x][node.y + 1]
        if right.type != Type.stone_wall:  # and right.type != Type.door:
            if right.type == Type.door and right.data.lower() in keys:
                node_successors.append(right)
            if right.type != Type.door:
                node_successors.append(right)
    except IndexError:
        pass

    return node_successors


def a_star(vault_map, node_start, node_goal, keys_achieved):
    for line in vault_map:
        for node in line:
            node.g = 0
            node.h = 0
            node.f = 0

    node_start.h = node_start.manhattan_distance(node_goal)
    open_list = [node_start]
    closed_list = []

    while open_list:
        node_current = open_list.pop(0)
        if node_current == node_goal:
            return node_current.g

        node_successors = get_node_successors(node_current, vault_map, keys_achieved)
        for node_successor in node_successors:
            node_successor_current_g = node_current.g + 1

            if node_successor in open_list:
                if node_successor.g <= node_successor_current_g:
                    continue
            elif node_successor in closed_list:
                if node_successor.g <= node_successor_current_g:
                    continue
                closed_list.remove(node_successor)
                node_successor.update_f()
                open_list.append(node_successor)
            else:
                node_successor.h = node_successor.manhattan_distance(node_goal)
                node_successor.update_f()
                open_list.append(node_successor)

            node_successor.g = node_successor_current_g
            node_successor.parent = node_current

        closed_list.append(node_current)
        open_list.sort(key=lambda x: x.f, reverse=False)

    if node_current != node_goal:
        return -1


if __name__ == '__main__':
    filename = sys.argv[1]

    with open(filename, 'r') as f:
        content = f.readlines()
        # build map
        vault_map = [[None for x in range(len(content[0]) - 1)] for y in range(len(content) - 1)]
        keys_to_search = []
        doors_to_search = []
        entrance = None
        for i in range(len(content) - 1):
            for j in range(len(content[i]) - 1):
                type = Type.from_value(content[i][j])
                data = None
                node = Node(x=i, y=j, type=type)
                if type == Type.key:
                    keys_to_search.append(node)
                    data = content[i][j]
                if type == Type.door:
                    doors_to_search.append(node)
                    data = content[i][j]
                if type == Type.entrance:
                    entrance = node
                    node.type = Type.open_passage
                node.data = data
                vault_map[i][j] = node

    total_distance = 0
    keys_achieved = []
    while keys_to_search:
        distances_keys = {}
        for key in keys_to_search:
            distance = a_star(vault_map, entrance, key, keys_achieved)
            if distance != -1:
                distances_keys[key] = distance

        closest_key = min(distances_keys, key=distances_keys.get)

        distances_doors = {}
        for door in doors_to_search:
            distance = a_star(vault_map, entrance, door, keys_achieved)
            if distance != -1:
                distances_doors[door] = distance

        if distances_doors:
            closest_door = min(distances_doors, key=distances_doors.get)
            if distances_doors[closest_door] <= distances_keys[closest_key]:
                total_distance += distances_doors[closest_door]
                vault_map[closest_door.x][closest_door.y] = Node(x=closest_door.x, y=closest_door.y,
                                                                 type=Type.open_passage)
                keys_achieved.remove(closest_door.data.lower())
                doors_to_search.remove(closest_door)
                entrance = closest_door
            else:
                total_distance += distances_keys[closest_key]
                keys_achieved.append(closest_key.data)
                entrance = closest_key
                keys_to_search.remove(closest_key)
        else:
            total_distance += distances_keys[closest_key]
            keys_achieved.append(closest_key.data)
            entrance = closest_key
            keys_to_search.remove(closest_key)

    print(total_distance)
