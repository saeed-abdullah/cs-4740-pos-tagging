import unittest2

from .. import probability

class ProbabilityTest(unittest2.TestCase):

    def setUp(self):
        self._tag_word = {"<s> <s>": 1, "Pierre NNP": 1, "Vinken NNP": 2,
                ", ,": 1, "61 CD": 1, "steadily RB": 1, "increasing VBG": 1,
                "net NN": 1, ". .": 1}

        self._unigram_count = {"<s>": 1, "NNP": 3, ",": 1, "CD": 1, "RB": 1,
                "VBG": 1, "NN": 1, ".": 1}

        self._bigram_count = {"NNP <s>": 1, "NNP NNP": 2, ", NNP": 1,
                "CD ,":1, "RB CD": 1, "VBG RB": 1, "NN VBG": 1, ". NN": 1}

        self._trigram_count = {"NNP NNP <s>": 1, "NNP NNP NNP": 1,
                ", NNP NNP": 1, "CD , NNP": 1, "RB CD ,": 1, "VBG RB CD": 1,
                "NN VBG RB": 1, ". NN VBG": 1}

    def test_probability_distribution(self):
        prob = probability.ProbabilityDistribution(self._tag_word,
                self._unigram_count)

        self.assertEqual(prob["Vinken NNP"], 2./3)
        self.assertEqual(prob[". ,"], 0)

    def test_smoother_probability_distribution(self):
        prob = probability.SmoothedDistribution(self._tag_word,
                self._unigram_count)

        self.assertEqual(prob["NONEXIST NNP"], 1./11)
        self.assertEqual(prob["Vinken NNP"], 3./11)

        prob = probability.SmoothedDistribution(self._bigram_count,
                self._unigram_count)

        self.assertEqual(prob["NNP <s>"], 2./9)
        self.assertEqual(prob[", NNP"], 2./11)






