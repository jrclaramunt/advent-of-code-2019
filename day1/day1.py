import sys
from math import floor


def calculate_fuel(mass):
    return floor(int(mass) / 3) - 2


if __name__ == '__main__':
    filename = sys.argv[1]

    with open(filename, 'r') as f:
        mass_list = f.readlines()

        fuel_required = 0
        additional_fuel_required = 0

        for mass in mass_list:

            fuel = calculate_fuel(mass)
            fuel_required += fuel
            while fuel > 0:
                additional_fuel_required += fuel
                fuel = calculate_fuel(fuel)

        print(f'Fuel required: {fuel_required}')
        print(f'Additional Fuel required: {additional_fuel_required}')
