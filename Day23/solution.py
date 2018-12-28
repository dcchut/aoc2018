from utils import load_input, get_numbers, manhattan_distance

class Nanobot:
    def __init__(self,_x, _y, _z, _r):
        self.x = _x
        self.y = _y
        self.z = _z
        self.r = _r

    def __repr__(self):
        return str((self.x,self.y,self.z,self.r))


puzzle_input = load_input('input.txt')

nanobots = []

for line in puzzle_input:
    x, y, z, r = get_numbers(line)
    nanobots.append(Nanobot(x,y,z,r))

nanobots.sort(key=lambda q:q.r, reverse=True)

# PART 1
r = nanobots[0]
nanobots_in_range = 0

for bot in nanobots:
    if manhattan_distance((r.x,r.y,r.z),(bot.x,bot.y,bot.z)) <= r.r:
        nanobots_in_range += 1

print('Part 1:', nanobots_in_range)

# PART 2
# For part 2, we use the Z3 solver as suggested by mserrano
# cdoe from: https://old.reddit.com/r/adventofcode/comments/a8s17l/2018_day_23_solutions/ecdbux2/?st=jq8f8wna&sh=30c83d9f
import z3

# absolute value function
def zabs(x):
    return z3.If(x >= 0, x, -x)

o = z3.Optimize()

# define formal integer variables x, y, and z
x, y, z = z3.Ints('x y z')

# for each bot, define a function in_range_[i] which is
# 1 if the selected bot is in range, and 0 otherwise
in_range = []

for (k, bot) in enumerate(nanobots):
    _x = bot.x
    _y = bot.y
    _z = bot.z
    _r = bot.r
    in_range.append(z3.Int(f"in_range_{k}"))
    # this defines the in_range[k] function
    o.add(in_range[k] == z3.If(zabs(x-_x)+zabs(y-_y)+zabs(z-_z) <= _r, 1, 0))

# variable for the number of bots in range from the current bot
bots_in_range = z3.Int('bots_in_range')
o.add(bots_in_range == sum(in_range))

# variable for the distance of the current bot from (0,0)
magnitude = z3.Int('magnitude')
o.add(magnitude == zabs(x) + zabs(y) + zabs(z))

# now, we want to maximise the number of bots in range,
# while minimising our distance from the origin
# the order here is important!
h1 = o.maximize(bots_in_range)
h2 = o.minimize(magnitude)

if o.check():
    print('Part 2:', o.lower(h2))
