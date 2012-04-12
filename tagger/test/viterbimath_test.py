#import unittest2
#from StringIO import StringIO

#import mock
#from mock import MagicMock, patch

#from .. import viterbimath
import sys
sys.path.append("..")
from viterbimath import ViterbiMath
import unittest

class DynamicT:
    def __init__(self, seq):
        self.seq = seq
        self.col = 0
        self.table = []

    def prob(self, m, n):
        return self.table[n][m]

    def update(self, col):
        self.table.append(col)
        self.col = self.col + 1
        return self

class VeterbiMathTest(unittest.TestCase):
    def setUp(self):
        self._tags = ["NN", "VB"]
        self._obsT = {"the NN": 0.1, "cat NN": 0.7, "is NN": 0.1, "pretty NN": 0.1,
            "the VB": 0.1, "cat VB": 0.1, "is VB": 0.7, "pretty VB": 0.1}
        self._transmBi = {"NN VB": 0.4, "NN NN": 0.1, "VB NN": 0.4, "VB VB": 0.1}
        self._transmTri = {"NN NN NN": 0.05, "NN NN VB": 0.2, "NN VB NN": 0.3, "NN VB VB": 0.1,
            "VB NN NN": 0.1, "VB NN VB": 0.1, "VB VB NN": 0.1, "VB VB VB": 0.05}

    def test_bigram_viterbi(self):
        dt = DynamicT("the cat is pretty")
        words = dt.seq.split()
        viterbi = ViterbiMath(self._obsT, self._transmBi, self._transmTri, self._tags)
        dt.update(viterbi.get_next_column(dt, 2, dt.col, words[dt.col]))
        dt.update(viterbi.get_next_column(dt, 2, dt.col, words[dt.col]))
        expected_table = [[0.1, 0.1], [0.027999999999999997, 0.004000000000000001]]
        actual_table = dt.table
        self.assertListEqual(expected_table, actual_table, "bigram test")

    def test_trigram_viterbi(self):
        dt = DynamicT("the cat is pretty")
        words = dt.seq.split()
        viterbi = ViterbiMath(self._obsT, self._transmBi, self._transmTri, self._tags)
        dt.update(viterbi.get_next_column(dt, 3, dt.col, words[dt.col]))
        dt.update(viterbi.get_next_column(dt, 3, dt.col, words[dt.col]))
        print dt.table
        expected_table = [[0.1, 0.1], [0.027999999999999997, 0.004000000000000001]]
        actual_table = dt.table
        self.assertListEqual(expected_table, actual_table, "trigram test")

if __name__ == "__main__":
    unittest.main()
