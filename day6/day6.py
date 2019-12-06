import sys


class Node:

    def __init__(self, data, father=None):
        self.data = data
        self.father = father

    def __str__(self):
        return f'Data: {self.data} - Father: {self.father}'


def path_to_origin(node):
    path = []
    while node.father is not None:
        path.append(node.data)
        node = node.father

    return path


if __name__ == '__main__':
    filename = sys.argv[1]

    with open(filename, 'r') as f:
        content = f.readlines()

        orbital_dict = {}

        for orbital_object in content:
            objects = orbital_object.split(')')
            obj_a = objects[0]
            obj_b = objects[1].strip()

            if orbital_dict.get(obj_a) is None:
                node_a = Node(data=obj_a)
                orbital_dict[obj_a] = node_a
            else:
                node_a = orbital_dict.get(obj_a)

            if orbital_dict.get(obj_b) is None:
                node_b = Node(data=obj_b, father=node_a)
                orbital_dict[obj_b] = node_b
            else:
                node_b = orbital_dict.get(obj_b)
                node_b.father = node_a

            orbital_dict[obj_b] = node_b

    total_orbits = 0
    for obj, node in orbital_dict.items():
        total_orbits += len(path_to_origin(node))

    print(f'Total direct and indirect orbits: {total_orbits}')

    node_san = orbital_dict.get('SAN')
    node_you = orbital_dict.get('YOU')

    path_san_to_origin = path_to_origin(node_san)
    path_you_to_origin = path_to_origin(node_you)

    common_orbits = list(set(path_san_to_origin) & set(path_you_to_origin))

    minimum_orbital_transfers = sys.maxsize
    for common_orbit in common_orbits:
        trasnfers = path_san_to_origin.index(common_orbit) - 1 + path_you_to_origin.index(common_orbit) - 1
        if trasnfers < minimum_orbital_transfers:
            minimum_orbital_transfers = trasnfers

    print(f'Minimum orbital transfers to reach Santa: {minimum_orbital_transfers}')
