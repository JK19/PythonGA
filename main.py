from reactor import Reactor
import time

elements = {
    "A": (3, 2),  # (price, weight)
    "B": (10, 7),
    "C": (23, 11),
    "Z": (0, 0)
}
alphabet = list(elements.keys())

MAX_WEIGHT = 315
STEPS = 10000
MAX_CONTAINERS = 30

def totalvalues(x):
    totalw, totalp = 0, 0
    for container in x:
        values = elements[container]
        totalp += values[0] * values[1]  # price per weight
        totalw += values[1]
    return totalw, totalp

def fitness(x):
    totalw, totalp = totalvalues(x)  # sum of total weight and value of the cargo configuration
    if totalw <= MAX_WEIGHT:  # if under max weight return it's value
        return totalp * totalw  # multiply so the fitness scales linearly
    else:  # return it's owerweight as negative value
        ow = totalw - MAX_WEIGHT
        return -ow

def main():
    
    solver = Reactor(6, MAX_CONTAINERS, alphabet, fitness, 0.4).addCores(3)
    
    start = time.time()
    
    solver.run(STEPS)
    res = solver.get_results()
    
    end = time.time()

    print("RESULTS:")
    print("ELAPSED: {} seconds".format(end - start))            
    for i in range(len(res)):
        solution = res[i]
        print("Solution {}:".format(i))
        print("\tFitness: {}".format(fitness(solution)))
        print("\tValues (W, P): {}".format(totalvalues(solution)))
        sortedRes = sorted(solution, key=lambda x: elements[x][1])  # sort by weight
        for j in range(0, len(sortedRes), 5):
            print("\t\t##### ##### ##### ##### #####")
            print("\t\t# {} # # {} # # {} # # {} # # {} #".format(sortedRes[j], sortedRes[j+1], sortedRes[j+2], sortedRes[j+3], sortedRes[j+4]))
            print("\t\t##### ##### ##### ##### #####")


if __name__ == '__main__':
    main()