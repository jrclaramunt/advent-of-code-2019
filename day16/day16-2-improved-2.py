import sys
from time import time

if __name__ == '__main__':
    filename = sys.argv[1]

    pattern = [0, 1, 0, -1]
    phases = 100
    t1 = time()
    with open(filename, 'r') as f:
        content = f.readlines()[0]
        input = list(map(lambda x: int(x), content))

        for phase in range(phases):

            # 1 - 1
            # 0(1) - 2
            # 0(2) - 3
            # 0(3) - 4
            # 0(4) - 5

            #     0       1        2       3       4       5        6       7
            # 1 * 1 + 2 * 0 + 3 * -1 + 4 * 0 + 5 * 1 + 6 * 0 + 7 * -1 + 8 * 0 = 4
            # 1 * 0 + 2 * 1 + 3 * 1 + 4 * 0 + 5 * 0 + 6 * -1 + 7 * -1 + 8 * 0 = 8

            # 1 * 0 + 2 * 0 + 3 * 1 + 4 * 1 + 5 * 1 + 6 * 0 + 7 * 0 + 8 * 0 = 2

            # 1 * 0 + 2 * 0 + 3 * 0 + 4 * 1 + 5 * 1 + 6 * 1 + 7 * 1 + 8 * 0 = 2
            # 1 * 0 + 2 * 0 + 3 * 0 + 4 * 0 + 5 * 1 + 6 * 1 + 7 * 1 + 8 * 1 = 6
            # 1 * 0 + 2 * 0 + 3 * 0 + 4 * 0 + 5 * 0 + 6 * 1 + 7 * 1 + 8 * 1 = 1
            # 1 * 0 + 2 * 0 + 3 * 0 + 4 * 0 + 5 * 0 + 6 * 0 + 7 * 1 + 8 * 1 = 5
            # 1 * 0 + 2 * 0 + 3 * 0 + 4 * 0 + 5 * 0 + 6 * 0 + 7 * 0 + 8 * 1 = 8

            gap = 1
            for i in range(len(input)):
                position = gap - 1
                result = 0

                pattern_index = 1

                while position < min(position + gap, len(input)):

                    for j in range(position, min(position + gap, len(input))):
                        assert(pattern[pattern_index] != 0)
                        if pattern_index == 1:
                            result += input[j]
                        else:
                            result -= input[j]

                    position += 2 * gap
                    pattern_index += 2
                    pattern_index %= 4

                input[i] = abs(int(list(str(result))[-1]))
                gap += 1

        t2 = time()
        print(f'Time: {t2 - t1}')
        print(''.join(list(map(lambda x: str(x), input[0:8]))))
        # 88323090

        # 01029498








