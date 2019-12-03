from enum import Enum
import sys


class Opcode(Enum):
    add = 1
    mul = 2
    halt = 99


class Computer:

    def __init__(self, intcode):
        self.intcode = intcode.copy()

    def set_registers(self, noun, verb):
        self.intcode[1] = noun
        self.intcode[2] = verb

    def restore_gravity_assist_program(self):
        i = 0
        while i < len(self.intcode):
            if self.intcode[i] == Opcode.add.value:
                a = self.intcode[self.intcode[i + 1]]
                b = self.intcode[self.intcode[i + 2]]
                self.intcode[self.intcode[i + 3]] = a + b
                i += 4
            elif self.intcode[i] == Opcode.mul.value:
                a = self.intcode[self.intcode[i + 1]]
                b = self.intcode[self.intcode[i + 2]]
                self.intcode[self.intcode[i + 3]] = a * b
                i += 4
            elif self.intcode[i] == Opcode.halt.value:
                break


if __name__ == '__main__':
    filename = sys.argv[1]
    output = 19690720

    with open(filename, 'r') as f:
        input = f.readlines()[0]
        original_intcode = list(map(lambda x: int(x), input.split(",")))

        noun = 12
        verb = 2
        computer = Computer(original_intcode)
        computer.set_registers(noun=noun, verb=verb)
        computer.restore_gravity_assist_program()
        print(f'Part 1 response: {computer.intcode[0]}')

        for noun in range(100):
            for verb in range(100):
                computer = Computer(original_intcode)
                computer.set_registers(noun=noun, verb=verb)
                computer.restore_gravity_assist_program()

                if computer.intcode[0] == output:
                    print(f'Part 2 response: {noun * 100 + verb}')