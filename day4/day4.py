import collections

if __name__ == '__main__':
    lower_range = 206938
    upper_range = 679128
    password_length = 6
    allowed_matching_digits = 2

    part_one_possibilities = 0
    part_two_possibilities = 0
    for i in range(lower_range, upper_range):
        candidate = [int(d) for d in str(i)]

        possible_password = True
        for c in range(len(candidate) - 1):
            if candidate[c] > candidate[c + 1]:
                possible_password = False
                break

        if possible_password is True:
            if len(set(candidate)) != password_length:
                part_one_possibilities += 1

            counter = collections.Counter(candidate)
            if allowed_matching_digits in counter.values():
                part_two_possibilities += 1

    print(f'Part one: {part_one_possibilities}')
    print(f'Part two: {part_two_possibilities}')


