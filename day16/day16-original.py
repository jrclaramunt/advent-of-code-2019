import sys
from time import time

if __name__ == '__main__':
    filename = sys.argv[1]

    initial_pattern = [0, 1, 0, -1]
    phases = 100
    t1 = time()
    with open(filename, 'r') as f:
        content = f.readlines()[0]
        input = list(map(lambda x: int(x), content))

        for phase in range(phases):
            pattern = initial_pattern.copy()

            for i in range(len(input)):
                pattern_index = 0
                count = 0
                index_counter = 0
                result = 0

                for j in range(len(input)):

                    if index_counter < i:
                        index_counter += 1
                    else:
                        pattern_index += 1
                        pattern_index = pattern_index % 4
                        index_counter = 0

                    r = input[j] * pattern[pattern_index]
                    result += r
                input[i] = abs(int(list(str(result))[-1]))

        t2 = time()
        print(f'Time: {t2 - t1}')
        print(''.join(list(map(lambda x: str(x), input[0:8]))))
        # 88323090








