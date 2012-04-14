# Viterbi Algorithm's Math/computation part
# viterbimath.py

from DynamicTable import DynamicTable

"""
Class:  ViterbiMath(observation_table, trans_matrix_bi, trans_matrix_tri, tags)

The caller of this class should expect to call the function
'predict(...)' only. The rest of the functions are internally used.
"""
class ViterbiMath:
    def __init__(self, observation_table, trans_matrix_bi, trans_matrix_tri, tags):
        """
        input
            observation_table
            trans_matrix_bi
            trans_matrix_tri: pass along None if you want to use bigram_model only.
            tags: a list of tags, e.g. ["NN" "VB"]
        """
        self.obsT = observation_table
        self.transmBi = trans_matrix_bi
        self.transmTri = trans_matrix_tri
        self.tags = tags

    def predict(self, word_seq, n):
        """
        Predicts the tag sequence of a word sequence 'word_seq' using 'n'-gram model.
        ----
        input
            word_seq: a list of word strings to predict the tag sequence
            n: either 2 (bigram) or 3 (trigram)

        returns a list of tag strings of the tag sequence predicted
        """
        dynamic_table = DynamicTable()
        seq_size = len(word_seq)
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
                for tag_prev2 in self.tags:
                    prev2_prob = dt.prob(c_prev2, tag_prev2)
                    trans2_prob = self.transmBi[tag_prev1 + " " + tag_prev2]
                    trans3_prob = self.transmTri[tag_cur + " " + tag_prev2 + " " + tag_prev1]
                    prob = obs_tag_prob * (0.5*trans2_prob + 0.5*trans3_prob) * prev2_prob
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

