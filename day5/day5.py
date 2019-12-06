from enum import Enum
import sys


class Opcode(Enum):
    add = 1
    mul = 2
    input = 3
    output = 4
    jump_if_true = 5
    jump_if_false = 6
    less_than = 7
    equals = 8
    halt = 99


class Mode(Enum):
    position = 0
    immediate = 1


class Computer:

    def __init__(self, intcode, input):
        self.intcode = intcode.copy()
        self.output = input

    def get_opcode(self, code):
        opcode = code
        if code > 100:
            data = [d for d in str(code)]
            opcode = int("".join(data[-2:]))

        return opcode

    def get_mode(self, code):
        if code > 100:
            data = [int(d) for d in str(code)]
            return {
                'a': data[-3],
                'b': data[-4] if len(data) > 3 else 0,
                'c': data[-5] if len(data) > 4 else 0
            }
        return {
            'a': 0,
            'b': 0,
            'c': 0
        }

    def get_value(self, mode, index):
        return self.intcode[self.intcode[index]] if mode == Mode.position.value else self.intcode[index]

    def run_diagnostic_program(self):
        i = 0
        output = self.output
        while i < len(self.intcode):

            opcode = self.get_opcode(self.intcode[i])
            modes = self.get_mode(self.intcode[i])

            if opcode == Opcode.add.value:
                a = self.get_value(modes['a'], i + 1)
                b = self.get_value(modes['b'], i + 2)
                self.intcode[self.intcode[i + 3]] = a + b
                i += 4

            elif opcode == Opcode.mul.value:
                a = self.get_value(modes['a'], i + 1)
                b = self.get_value(modes['b'], i + 2)
                self.intcode[self.intcode[i + 3]] = a * b
                i += 4

            elif opcode == Opcode.input.value:
                a = self.intcode[i + 1]
                self.intcode[a] = output
                i += 2

            elif opcode == Opcode.output.value:
                a = self.get_value(modes['a'], i + 1)
                output = a
                self.output = a
                i += 2

            elif opcode == Opcode.jump_if_true.value:
                a = self.get_value(modes['a'], i + 1)
                b = self.get_value(modes['b'], i + 2)
                if a != 0:
                    i = b
                else:
                    i += 3

            elif opcode == Opcode.jump_if_false.value:
                a = self.get_value(modes['a'], i + 1)
                b = self.get_value(modes['b'], i + 2)
                if a == 0:
                    i = b
                else:
                    i += 3

            elif opcode == Opcode.less_than.value:
                a = self.get_value(modes['a'], i + 1)
                b = self.get_value(modes['b'], i + 2)
                if a < b:
                    self.intcode[self.intcode[i + 3]] = 1
                else:
                    self.intcode[self.intcode[i + 3]] = 0
                i += 4

            elif opcode == Opcode.output.equals.value:
                a = self.get_value(modes['a'], i + 1)
                b = self.get_value(modes['b'], i + 2)
                if a == b:
                    self.intcode[self.intcode[i + 3]] = 1
                else:
                    self.intcode[self.intcode[i + 3]] = 0
                i += 4

            elif opcode == Opcode.halt.value:
                break


if __name__ == '__main__':
    filename = sys.argv[1]

    with open(filename, 'r') as f:
        content = f.readlines()[0]
        original_intcode = list(map(lambda x: int(x), content.split(",")))

        input = 1
        computer = Computer(original_intcode, input)
        computer.run_diagnostic_program()
        print(f'Part 1 response: {computer.output}')

        input = 5
        computer = Computer(original_intcode, input)
        computer.run_diagnostic_program()
        print(f'Part 2 response: {computer.output}')
