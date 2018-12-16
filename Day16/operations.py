def addr(register, a, b, c):
    register[c] = register[a] + register[b]
    return register


def addi(register, a, b, c):
    register[c] = register[a] + b
    return register


def mulr(register, a, b, c):
    register[c] = register[a] * register[b]
    return register


def muli(register, a, b, c):
    register[c] = register[a] * b
    return register


def banr(register, a, b, c):
    register[c] = register[a] & register[b]
    return register


def bani(register, a, b, c):
    register[c] = register[a] & b
    return register


def borr(register, a, b, c):
    register[c] = register[a] | register[b]
    return register


def bori(register, a, b, c):
    register[c] = register[a] | b
    return register


def setr(register, a, b, c):
    register[c] = register[a]
    return register


def seti(register, a, b, c):
    register[c] = a
    return register


def gtir(register, a, b, c):
    if a > register[b]:
        register[c] = 1
    else:
        register[c] = 0
    return register


def gtri(register, a, b, c):
    if register[a] > b:
        register[c] = 1
    else:
        register[c] = 0
    return register


def gtrr(register, a, b, c):
    if register[a] > register[b]:
        register[c] = 1
    else:
        register[c] = 0
    return register


def eqir(register, a, b, c):
    if a == register[b]:
        register[c] = 1
    else:
        register[c] = 0
    return register


def eqri(register, a, b, c):
    if register[a] == b:
        register[c] = 1
    else:
        register[c] = 0
    return register


def eqrr(register, a, b, c):
    if register[a] == register[b]:
        register[c] = 1
    else:
        register[c] = 0
    return register