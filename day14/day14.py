import sys
from math import ceil


class Element:

    def __init__(self, amount, name, elements=None):
        self.amount = amount
        self.name = name
        self.elements = elements

    def __str__(self):
        return self.name


def calculate_ore(output_list, elements_map, rest_dict):

    if not output_list:
        return 0

    output = output_list.pop(0)

    try:
        new_output = elements_map[output.name]
        new_elements = new_output.elements
        if output.amount > new_output.amount:
            amount_needed = ceil(output.amount / new_output.amount)
            if rest_dict.get(output.name) is not None:
                output.amount -= rest_dict.get(output.name)
                if output.amount < 0:
                    output.amount = 0
                    rest_dict[output.name] -= output.amount
                else:
                    del rest_dict[output.name]

            rest = output.amount % new_output.amount
            if rest != 0:
                rest_dict[output.name] = rest
            for elem in new_elements:
                if elem.name != 'ORE':
                    elem.amount *= amount_needed
                    if rest_dict.get(elem.name) is not None:
                        elem.amount -= rest_dict.get(elem.name)
                        if elem.amount < 0:
                            elem.amount = 0
                            rest_dict[elem.name] -= elem.amount
                        else:
                            del rest_dict[elem.name]
                else:
                    return elem.amount * amount_needed + calculate_ore(new_elements + output_list, elements_map, rest_dict)
        else:
            if rest_dict.get(output.name) is not None:
                rest_dict[output.name] += new_output.amount - output.amount
            else:
                rest_dict[output.name] = new_output.amount - output.amount
        return calculate_ore(new_elements + output_list, elements_map, rest_dict)

    except KeyError:
        return calculate_ore(output_list, elements_map, rest_dict)


if __name__ == '__main__':
    filename = sys.argv[1]
    formulas = {}

    with open(filename, 'r') as f:
        reactions = f.readlines()
        for reaction_line in reactions:
            reaction = reaction_line.split('=>')
            input = reaction[0]
            input_elements = input.split(',')
            elements = []
            for input_element in input_elements:
                element = input_element.strip().split(' ')
                amount = int(element[0])
                name = element[1]
                elements.append(Element(amount, name))

            output = reaction[1].strip()
            output_elements = output.split(' ')
            amount = int(output_elements[0])
            name = output_elements[1]
            formulas[name] = Element(amount, name, elements)

        print(calculate_ore(formulas['FUEL'].elements, formulas, {}))




