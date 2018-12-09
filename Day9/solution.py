from utils import load_input, Node, CircularDoublyLinkedList
from collections import defaultdict


def winning_score(players, highest_marble):
    cdll = CircularDoublyLinkedList()

    current = Node(0)
    cdll.append(current)
    scores = defaultdict(int)

    for key in range(1, highest_marble + 1):
        # if key is a multiple of 23
        if key % 23 == 0:
            scores[key % players] += key

            # we go 7 marbles counter-clockwise
            mb = current.prev.prev.prev.prev.prev.prev.prev

            scores[key % players] += mb.data

            # now remove mb from our LL
            current = mb.next
            cdll.remove(mb)
        else:
            # get the current marble
            mb = Node(key)
            # insert marble after marble after this one
            cdll.insert(current.next, mb)
            current = mb

    return max(list(scores.values()))


def main():
    # Get the number of players, and the (base) highest marble0
    players, _, _, _, _, _, base_highest_marble, _ = load_input('input.txt')[0].split()

    # convert to integers
    players = int(players)
    base_highest_marble = int(base_highest_marble)

    print('Part 1', winning_score(players, base_highest_marble))
    print('Part 2', winning_score(players, base_highest_marble * 100))


if __name__ == '__main__':
    main()
