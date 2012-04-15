import sys
sys.path.append("..")
from viterbimath import ViterbiMath
from DynamicTable import DynamicTable
import unittest

class VeterbiMathTest(unittest.TestCase):
    def setUp(self):
        self._tags = ["NN", "VB"]
        self._obsT = {"the NN": 0.1, "cat NN": 0.7, "is NN": 0.1, "pretty NN": 0.1,
            "the VB": 0.1, "cat VB": 0.1, "is VB": 0.7, "pretty VB": 0.1}
        self._transmBi = {"NN VB": 0.4, "NN NN": 0.1, "VB NN": 0.4, "VB VB": 0.1}
        self._transmTri = {"NN NN NN": 0.05, "NN NN VB": 0.3, "NN VB NN": 0.3, "NN VB VB": 0.05,
            "VB NN NN": 0.1, "VB NN VB": 0.1, "VB VB NN": 0.05, "VB VB VB": 0.05}
        self._wordSeq = ["the", "cat", "is", "pretty"]

        self._unigramCount = "data/unigram_count.json"
        self._trigramCount = "data/trigram_count.json"
        self._bigramCount = "data/bigram_count.json"
        self._tagWordCount = "data/tag_word_count.json"
        self._outputFile = "data/output.pos"
        self._testFile = "data/test.pos"

    def test_bigram_viterbi(self):
        dt = DynamicTable()
        viterbi = ViterbiMath(self._obsT, self._transmBi, self._transmTri, self._tags)
        col = 0
        dt.update(viterbi.get_next_column(dt, 2, col, self._wordSeq[col]))
        col = col + 1
        dt.update(viterbi.get_next_column(dt, 2, col, self._wordSeq[col]))
        expected_table = [{'VB': 0.1, 'NN': 0.1},
            {'VB': 0.004000000000000001, 'NN': 0.027999999999999997}]
        actual_table = dt.probs
        self.assertListEqual(expected_table, actual_table, "do_bigram() probability computation test")

    def test_trigram_viterbi(self):
        dt = DynamicTable()
        viterbi = ViterbiMath(self._obsT, self._transmBi, self._transmTri, self._tags)
        col = 0
        dt.update(viterbi.get_next_column(dt, 3, col, self._wordSeq[col]))
        col = col + 1
        dt.update(viterbi.get_next_column(dt, 3, col, self._wordSeq[col]))
        expected_table = [{'VB': 0.1, 'NN': 0.1}, {'VB': 0.004000000000000001, 'NN': 0.027999999999999997}] 
        actual_table = dt.probs
        self.assertListEqual(expected_table, actual_table, "do_trigram() probability computation test")

    def test_predict_bigram(self):
        viterbi = ViterbiMath(self._obsT, self._transmBi, self._transmTri, self._tags)
        expected_tag_seq = ['VB', 'NN', 'VB', 'NN']
        actual_tag_seq = viterbi.predict(self._wordSeq, 2)
        self.assertListEqual(expected_tag_seq, actual_tag_seq, "predict tag seq using bigram model") 
        
    def test_predict_trigram(self):
        viterbi = ViterbiMath(self._obsT, self._transmBi, self._transmTri, self._tags)
        expected_tag_seq = ['NN', 'VB', 'NN', 'NN'] 
        actual_tag_seq = viterbi.predict(self._wordSeq, 3)
        self.assertListEqual(expected_tag_seq, actual_tag_seq, "predict tag seq using trigram model") 

    def test_run_bigram(self):
        viterbi = ViterbiMath(self._unigramCount, self._bigramCount,
            self._trigramCount, self._tagWordCount)
        expected_tag_seq = "<s> <s>\nDT the\nNN cat\nVBZ is\nRB pretty\n. .\n" 
        viterbi.run(self._testFile, self._outputFile, 2)
        actual_tag_seq = open(self._outputFile, 'r').read()
        self.assertEquals(expected_tag_seq, actual_tag_seq, "run bigram test")

    def test_run_trigram(self):
        viterbi = ViterbiMath(self._unigramCount, self._bigramCount,
            self._trigramCount, self._tagWordCount)
        expected_tag_seq = "FW <s>\nFW the\nFW cat\nFW is\nIN pretty\n. .\n" 
        viterbi.run(self._testFile, self._outputFile, 3)
        actual_tag_seq = open(self._outputFile, 'r').read()
        self.assertEquals(expected_tag_seq, actual_tag_seq, "run trigram test")


if __name__ == "__main__":
    unittest.main()
