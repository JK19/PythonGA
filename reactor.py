from basicGeneRoutines.BGM import randpopulation
from basicGeneRoutines.LifeCycle import cycle
from multiprocessing import Queue  # usable with thread or process


class Reactor(object):
    """
    Reactor and container of genetic algorithm
    """
    def __init__(self, size, chromolen, alphabet, fitnessfunc, pmut, sortfunc=None, engine="process"):
        """
        Params:
            size (int): Number of individuals in reactor population
            chromolen (int): Number of components in a individual (chromosome)
            alphabet (string[]): List with the string representation of each possible gene
            fitnessfunc (func): Function receiving a chromosome and returning a int
            pmut (float): Probability of mutating an individual in each population
            sortfunc (func): Overrides the default sorting function based on fitness
            engine (string): Type of paralellism used ("process" or "thread")
        """
        self.size = size
        self.chromolen = chromolen
        self.alphabet = alphabet
        self.fitness = fitnessfunc
        self.pmut = pmut
        if sortfunc is None:
            self.sortfunc = self.fitness
        else:
            self.sortfunc = sortfunc
        self.engine = engine
        self.cores = 1
        self.running_cores = []
        self.result_queue = Queue()
        self.population = randpopulation(self.size, self.chromolen, self.alphabet)

    def addCores(self, cores):
        if self.cores + cores >= 1:
            self.cores += cores
        return self

    def run(self, steps, ongeneration=None):
        #TODO: add a sync=True parameter to run a task in local thread or all task in paralell

        # create cores
        if self.engine.lower() == "process":
            from multiprocessing import Process as Task
        elif self.engine.lower() == "thread":
            from threading import Thread as Task
        else:
            raise ValueError("Unknown engine {}".format(self.engine))

        for i in range(self.cores):
            # tasks.append(Process(target=self._loop, args=(i, steps, ongeneration, results)))
            self.running_cores.append(Task(target=self._loop, args=(i, steps, ongeneration, self.result_queue)))

        # launch
        for task in self.running_cores:
            task.start()

        # create local process
        # tasks.append(Process(target=self._loop, args=(0, steps, ongeneration, results)))
        # self._loop(0, steps, ongeneration, results)

        # join launched processes
        # for task in tasks:
        #     task.join()

        # return [results.get() for _ in range(results.qsize())]
        return self

    def get_results(self):
        for task in range(len(self.running_cores)):
            self.running_cores.pop().join()
        return [self.result_queue.get() for _ in range(self.result_queue.qsize())]

    def _loop(self, core, steps, ongeneration=None, queue=None):

        pop = self.population[:]  # local copy
        top = None

        for step in range(steps):

            pop, best = cycle(
                population=pop,
                alphabet=self.alphabet,
                pmut=self.pmut,
                sortfunc=self.sortfunc
            )

            if ongeneration is not None:
                ongeneration(step, core, best)

            if top is None:
                top = best

            if self.fitness(best) > self.fitness(top):
                top = best

        if queue is not None:
            queue.put(top)
            return
        else:
            return top
