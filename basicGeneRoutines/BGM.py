import random as __rand


def crossover(a, b, point=None):
    if not point:
        point = __rand.randint(0, len(a)-1)
    ret_a = a[:]  # copy, not reference
    ret_b = b[:]

    tmp = ret_a[point:]
    ret_a[point:] = ret_b[point:]
    ret_b[point:] = tmp

    return ret_a, ret_b


def mutate(indiv, pmut, alphabet):
    if __rand.random() < pmut:
        ret = indiv[:]
        randpoint = __rand.randint(0, len(indiv)-1)
        ret[randpoint] = __rand.choice(alphabet)
        return ret, True
    else:
        return indiv, False


def randpopulation(size, chromolen, alphabet):
    ret = []
    for i in range(size):
        indiv = []
        for j in range(chromolen):
            indiv.append(__rand.choice(alphabet))
        ret.append(indiv)
    return ret
