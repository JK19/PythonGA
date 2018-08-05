import unittest
from unittest.mock import patch
from basicGeneRoutines.LifeCycle import cycle


class LCtest(unittest.TestCase):

    @patch("random.randint", return_value=1)  # point for crossover and for mutation
    def test_cycle(self, mutate):

        population = [
            ["A"]*4,
            ["B"]*4,
            ["C"]*4,
            ["D"]*4
        ]

        def fitness(chromo):
            return (chromo.count("A")*3) + (chromo.count("B")*2) + (chromo.count("C")*1)

        pop_res, best = cycle(
            population=population,
            alphabet=["A", "B", "C", "D"],
            pmut=0.0,
            sortfunc=lambda x: fitness(x)
        )

        err = "crossover not applied"
        self.assertEqual(pop_res[0], ["A", "B", "B", "B"], msg=err)
        self.assertEqual(pop_res[1], ["B", "A", "A", "A"], msg=err)
        err = "unable to extract the best from population"
        self.assertEqual(best, ["A", "A", "A", "A"], msg=err)


if __name__ == '__main__':
    unittest.main()
