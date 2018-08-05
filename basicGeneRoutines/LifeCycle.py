from basicGeneRoutines.BGM import *


def cycle(**config):
    """
    Parameters:
        population=[]
        alphabet=[]
        pmut=float
        sortfunc=function
    """
    # unpackage parameters
    pop = config["population"]
    chromolen = len(pop[0])  # config["chromolen"]
    alphabet = config["alphabet"]
    pmut = config["pmut"]

    # sort population by fitness or equivalent
    sortfunc = config["sortfunc"]
    pop.sort(key=sortfunc, reverse=True)

    # get most performant indivs
    alpha = pop[0]
    beta = pop[1]
    best = alpha

    alpha, beta = crossover(alpha, beta)

    # rebuild population
    pop = [alpha, beta] + randpopulation(len(pop)-2, chromolen, alphabet)

    pop = list(map(lambda x: mutate(x, pmut, alphabet)[0], pop))

    return pop, best
