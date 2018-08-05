import unittest
from unittest.mock import patch
from basicGeneRoutines.BGM import *


class BGMtest(unittest.TestCase):

    def test_crossover(self):
        a_orig = ["A", "A", "A"]
        b_orig = ["B", "B", "B"]

        a_orig, b_orig = crossover(a_orig, b_orig, point=2)

        err_msg = "failed to crossover individuals"
        self.assertEqual(a_orig, ["A", "A", "B"], msg=err_msg)
        self.assertEqual(b_orig, ["B", "B", "A"], msg=err_msg)

    @patch("random.randint", return_value=1)  # gene to mutate
    def test_mutate(self, randint):
        orig = ["A", "B", "C"]
        res, mut = mutate(orig, 1, ["X"])
        self.assertEqual(mut, True, msg="didn't return True with pMut=1")
        self.assertEqual(res, ["A", "X", "C"], msg="failed to mutate individual")

    def test_randPopulation(self):
        res = randpopulation(6, 4, ["X"])
        self.assertEqual(len(res), 6, msg="wrong number of individuals")
        self.assertEqual(len(res[0]), 4, msg="wrong chromosome length")


if __name__ == '__main__':
    unittest.main()
