from collections import defaultdict

from utils import load_input


def get_digit(number, n):
    return number // 10 ** n % 10


def power_level(x, y, serial):
    rack_id = x + 10

    pwr = rack_id * y
    pwr += serial
    pwr *= rack_id

    pwr = get_digit(pwr, 2)
    pwr -= 5

    return pwr


def summed_area_table(serial_number):
    sat = defaultdict(int)

    for y in range(1, 301):
        for x in range(1, 301):
            sat[(x, y)] = power_level(x, y, serial_number) + sat[(x, y - 1)] + sat[(x - 1, y)] - sat[(x - 1, y - 1)]

    return sat


def max_power_level(size, sat):
    power_levels = {(x, y): rectangle_power(x, y, size, sat) for x in range(1, 301 - size) for y in
                    range(1, 301 - size)}
    m = max(power_levels, key=power_levels.get)
    return m[0], m[1], power_levels[m]


def rectangle_power(x, y, size, sat):
    # get the total power of the rectangle whose top-left coordinate is (x,y),
    # with side length size
    return sat[(x + size - 1, y + size - 1)] - sat[(x + size - 1, y - 1)] - sat[(x - 1, y + size - 1)] + sat[
        (x - 1, y - 1)]


def main():
    # get the list of step orderings
    serial_number = int(load_input('input.txt')[0])
    sat = summed_area_table(serial_number)

    # for part 2
    max_pos = None
    max_power = None
    max_size = None

    for size in range(3, 300):
        x, y, power = max_power_level(size, sat)
        if size == 3:
            print(f"Part 1: {x}, {y}, Power: {power}")
        if max_power is None or power > max_power:
            max_power = power
            max_pos = (x, y)
            max_size = size

    print(f"Part 2: {max_pos[0]}, {max_pos[1]}, Size: {max_size}")


if __name__ == '__main__':
    main()
