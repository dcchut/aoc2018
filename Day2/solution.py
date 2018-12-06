from utils import load_input
from collections import Counter
from itertools import combinations


def part1(id_list):
    two_count = 0
    three_count = 0

    # count how many IDs contain at least one letter twice,
    # and how many IDs contain at least one letter thrice
    for i in id_list:
        counter = Counter(i).values()
        if 2 in counter:
            two_count += 1
        if 3 in counter:
            three_count += 1

    # the checksum is the result of multiplying these two counts together
    return two_count * three_count


# count how many characters apart two words of the same length are
def word_difference(word1, word2):
    return sum(1 for i in range(0, len(word1)) if word1[i] != word2[i])


def part2(id_list):
    # find the pair of IDs with the smallest word difference
    minimal_word = min(combinations(id_list, 2), key=lambda q: word_difference(*q))

    # now find the common ground between the two words
    return ''.join(letter for (k, letter) in enumerate(minimal_word[0]) if minimal_word[1][k] == letter)


def main():
    id_list = load_input('input.txt')

    print('Part 1:', part1(id_list))
    print('Part 2:', part2(id_list))


if __name__ == '__main__':
    main()
