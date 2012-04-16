# Viterbi Algorithm's Math/computation part
# viterbimath.py

from DynamicTable import DynamicTable
from probability import SmoothedDistribution
from probability import ProbabilityDistribution
import json
import math

"""
Class:  ViterbiMath(observation_table, trans_matrix_bi, trans_matrix_tri, tags)

The caller of this class should expect to call the function
'predict(...)' only. The rest of the functions are internally used.
"""
class ViterbiMath:
    def __init__(self, unigram_count, bigram_count, trigram_count, tag_word_count, vocab_count):
        """
        input
            unigram_count = trigram_count.json filepath
            bigram_count = bigram_count.json filepath
            trigram_count = tag_word_count.json filepath
            tag_word_count = "unigram_count.json" filepath
        """
        if isinstance(tag_word_count, str):
            with open(tag_word_count) as f:
                tag_word_dict = json.loads(f.read())
            with open(unigram_count) as f:
                unigram_dict = json.loads(f.read())
            with open(bigram_count) as f:
                bigram_dict = json.loads(f.read())
            with open(trigram_count) as f:
                trigram_dict = json.loads(f.read())
            with open(vocab_count) as f:
                vocab_dict = json.loads(f.read())
            
            self.obsT = SmoothedDistribution(tag_word_dict, unigram_dict, vocab_dict)
            self.transmBi = SmoothedDistribution(bigram_dict, unigram_dict, vocab_dict)
            self.transmTri = SmoothedDistribution(trigram_dict, unigram_dict, vocab_dict)
            self.tags = unigram_dict.keys()
        else:
            self.tags = tag_word_count
            self.obsT = unigram_count
            self.transmBi = bigram_count
            self.transmTri = trigram_count

    def run(self, testfilename, outputfilename, n):
        word_seqs = open(testfilename, 'r').read().strip().split("\n")

        word_seq = []
        words = []
        tags = []
        
        i = 0
        for word in word_seqs:
            if word == "<s>":
                if len(word_seq) > 0:
                    tag_seq = self.predict(word_seq, n)
                    words = words + word_seq
                    tags = tags + tag_seq
                print i
                i += 1
                word_seq = []
            word_seq.append(word)

        tag_seq = self.predict(word_seq, n)
        words = words + word_seq
        tags = tags + tag_seq

        lines = []
        for (w, t) in zip(words, tags):
            lines.append(t + " " + w)

        open(outputfilename, 'w').write("\n".join(lines))

    def predict(self, word_seq, n):
        """
        Predicts the tag sequence of a word sequence 'word_seq' using 'n'-gram model.
        ----
        input
            word_seq: a list of word strings to predict the tag sequence
            n: either 2 (bigram) or 3 (trigram)

        returns a list of tag strings of the tag sequence predicted
        """
        seq_size = len(word_seq)
        if seq_size <= 0:
            return []
        dynamic_table = DynamicTable()
        for c in xrange(0,seq_size):
            next_col = self.get_next_column(dynamic_table, n, c, word_seq[c])
            dynamic_table.update(next_col)
        
        last_c = seq_size - 1
        last_col = dynamic_table.probs[last_c]
        last_best_tag = max(last_col, key=last_col.get)
        return dynamic_table.full_path(last_c, last_best_tag)

    def get_next_column(self, dynamic_table, n, c, word):
        """
        Internally used.
        Computes the probabilities of all the states'/tags' occurances for the
        current word in the sentnece given using 'n'-gram model.
        Currently, only bi- and tri- gram models are available.
        ----
        input
            dynamic_table: the dynamic table that has been filled out so far
                for the prediction.
            n: either 2(bigram viterbi) or 3(trigram viterbi)
            c: current column number, or the current location in the word
                sequence, c>=0
            word: current observation in the word sequence.
        
        returns a list containing the values for the next column of the
            dynamic_table for the current observation word.
        """
        if n==2:
            return self.do_bigram(dynamic_table, c, word)
        elif n==3:
            return self.do_trigram(dynamic_table, c, word)
        else:
            print "Wrong Input Value for n. Choose between 2 and 3."
            return None

    def do_bigram(self, dt, c, word):
        """
        Internally used within the class
        Compute Viterbi Algorithm using a bigram model.
        ----
        input
            dt: an instance of DynamicTable containing the probabilities of the previous states
            c: non-negative integer of the current location in the word sequence
            word: string of the current word in the word sequence

        returns a list of probabilities of possible tag sequences for 'word', or the probabilities
            to fill in the next column 'c' in the dynamic table 'dt'
        """
        if c==0:
            return self.first_column(word)
        
        next_column = {}
        c_prev = c - 1
        for tag_cur in self.tags:
            max_prob = 0.0
            max_tag_prev = None
            max_tuple = (max_prob, max_tag_prev)
            obs_tag_prob = self.obsT[word + " " + tag_cur]

            for tag_prev in self.tags:
                prev_prob = dt.prob(c_prev, tag_prev)
                trans_prob = self.transmBi[tag_cur + " " + tag_prev]
                prob = obs_tag_prob * trans_prob * prev_prob
                max_tuple = max(max_tuple, (prob, tag_prev))

            next_column[tag_cur] = max_tuple
        return next_column

    def do_trigram(self, dt, c, word):
        """
        Internally used within the class
        Compute Biterbi Algorithm using a trigram model.
        ----
        input
            dt: an instance of DynamicTable containing the probabilities of the previous states
            c: non-negative integer of the current location in the word sequence
            word: string of the current word in the word sequence

        returns a list of probabilities of possible tag sequences for 'word', or the probabilities
            to fill in the next column 'c' in the dynamic table 'dt'
        """
        if c<2:
            return self.do_bigram(dt, c, word)

        next_column = {}
        c_prev1 = c - 1
        c_prev2 = c - 2
        for tag_cur in self.tags:
            max_prob = 0.0
            max_tag_prev = None
            max_tuple = (max_prob, max_tag_prev)
            obs_tag_prob = self.obsT[word + " " + tag_cur]

            for tag_prev1 in self.tags:
                tag_prev2 = dt.last(c_prev1, tag_prev1)
                prev2_prob = dt.prob(c_prev2, tag_prev2)
                trans_prob = self.transmTri[tag_cur + " " + tag_prev2 + " " + tag_prev1]
                prob = obs_tag_prob * trans_prob * prev2_prob
                max_tuple = max(max_tuple, (prob, tag_prev1))
            
            next_column[tag_cur] = max_tuple
        return next_column

    def first_column(self, word):
        """
        Internally used within the class.
        Computes the probabilities of tagging the first word in the given word sequence.
        ----
        input
            word: string of the first word of the word sequence

        returns a list of probabilities of possible tags for 'word', or the probabilities to
            fill in the first column of the dynamic table of the veterbi algorithm
        """
        next_column = {}
        for tag in self.tags:
            next_column[tag] = (self.obsT[word + " " + tag], "")
        return next_column

