import sys
from enum import Enum


class Color(Enum):
    black = '0'
    white = '1'
    transparent = '2'

    def character(self):
        characters = {
            self.black.value: '·',
            self.white.value: '#',
            self.transparent.value: ' '
        }
        return characters[self.value]


if __name__ == '__main__':
    filename = sys.argv[1]

    width = 25
    height = 6
    image = [[Color.transparent.value for i in range(width)] for j in range(height)]

    with open(filename, 'r') as f:
        content = f.readlines()[0]

        i = 0
        layers = []
        min_blacks = sys.maxsize
        layer_with_less_black = None
        layer_size = width * height

        while i < len(content):
            layer = content[i:i+layer_size]

            blacks = layer.count(Color.black.value)
            if blacks < min_blacks:
                min_blacks = blacks
                layer_with_less_black = layer

            layers.append(layer)
            i += layer_size
        white_amount = layer_with_less_black.count(Color.white.value)
        transparent_amount = layer_with_less_black.count(Color.transparent.value)

        print(f'Part 1 Response {white_amount * transparent_amount}')
        print('Part 2: Response')
        for i in range(height):
            for j in range(width):
                for layer in layers:
                    pixel = layer[i * width + j]
                    if pixel != Color.transparent.value:
                        image[i][j] = Color(pixel).character()
                        break

        for j in range(height):
            print(''.join(image[j]))