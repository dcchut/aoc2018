from utils import load_input, mapstr


def combine_recipes(r1, r2):
    s = r1 + r2
    return [int(q) for q in str(s)]


def get_recipes(max_recipes, key=None):
    # get all recipes until we have at least max_recipes
    elves = [0, 1]
    recipes = [3, 7]

    while len(recipes) < max_recipes:
        # first, combine the two recipes
        new_recipes = combine_recipes(recipes[elves[0]], recipes[elves[1]])
        recipes += new_recipes

        # then shift each elf
        elves = [(elves[0] + 1 + recipes[elves[0]]) % len(recipes), (elves[1] + 1 + recipes[elves[1]]) % len(recipes)]

    return recipes


def main():
    # get the list of step orderings
    key = int(load_input('input.txt')[0])

    # get the 10 recipes after our puzzle input
    recipes = get_recipes(key + 10)
    print('Part 1:', ''.join(mapstr(recipes[key:key + 10])))

    # we keep generating recipes until our key appears
    recipes = get_recipes(25000000)
    
    # find the first place the key occurs in our recipe list
    print('Part 2:', ''.join(mapstr(recipes)).find(str(key)))


if __name__ == '__main__':
    main()
