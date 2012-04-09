# Viterbi Algorithm's Math/computation part
# viterbimath.py

"""
Class:  ViterbiMath(observation_table, trans_matrix_bi, trans_matrix_tri)
"""
class ViterbiMath:
    def __init__(observation_table, trans_matrix_bi, trans_matrix_tri):
        """
        input
            observation_table
            trans_matrix_bi
            trans_matrix_tri: pass along None if n=2.
        """
        self.obsT = observation_table
        self.transmBi = trans_matrix_bi
        self.transmTri = trans_matrix_tri
    
    def getNextColumn(self, dynamic_table, n):
        """
        Computes the probabilities of all the states'/tags' occurances for the
        current word in the sentnece given using 'n'-gram model.
        Currently, only bi- and tri- gram models are available.
        ----
        input
            dynamic_table: the dynamic table that has been filled out so far
                for the prediction.
            n: either 2(bigram viterbi) or 3(trigram viterbi)
        
        returns a list containing the values for the next column of the
            dynamic_table for the current observation word.
        """
        if n==2:
            return doBigram(self, dynamic_table)
        elif n==3:
            return doTrigram(self, dynamic_table)
        else:
            print "Wrong Input Value for n. Choose between 2 and 3."
            return None

    def doBigram(self, dt):
        """
        Internally used within the class
        """

    def doTrigram(self, dt):
        """
        Internally used within the class
        """
