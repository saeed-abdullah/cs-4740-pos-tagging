class DynamicTable:

    def __init__(self):
        """
        initializes internal data structures for viterbi representation
        """
        # probs and lasts are both lists that will be populated with
        # dictionaries (to allow for non-numeric indices
        self.probs = []
        self.lasts = []

    def prob(self, m, n):
        """
        Returns the probability of the path of predictions ending in
        last(m, n)
        ----
        input
            m:  row index to be queried
            n:  column index to be queried
        """
        return self.probs[m][n]

    def last(self, m ,n):
        """
        Returns the last word in the sequence that produced
        the probability stored at prob(m, n)
        ----
        input
            m:  row index to be queried
            n:  column index to be queried
        """
        return self.lasts[m][n]

    def full_path(self, m, n):
        """
        Returns the full path that produces the probability given at
        prob(m, n)
        ----
        input
            m:  row index to be queried
            n:  column index to be queried
        """
        path = [n]
        while m > 0:
            n = self.lasts[m][n]
            path += [n]
            m -= 1
        path.reverse()
        return path

    def update(self, col):
        """
        Updates internal data structures by adding a column that represents
        one step of a Viterbi algorithm's computations.
        ----
        input
            col:  full column of output from a Viterbi algorithm.  Must agree
                  in size with current data structures.

                  Current implementation assumes that the output of viterbi
                  will be a dict of the form (key -> (prob, last)) for each
                  element of the column.  This can be changed as necessary.

                  It is important to note that 'last' and 'key' must be of the
                  same type or the last and path functions will not operate
                  correctly

        returns True if column is properly sized, False otherwise
        """
        if self.probs == []:
            self.probs += [{}]
            self.lasts += [{}]
            for key in col.keys():
                (prob, last) = col[key]
                self.probs[0][key] = prob
                self.lasts[0][key] = last
            return True
        elif len(self.probs[0].keys()) == len(col.keys()):
            n = len(self.probs)
            self.probs += [{}]
            self.lasts += [{}]
            for key in col.keys():
                (prob, last) = col[key]
                self.probs[n][key] = prob
                self.lasts[n][key] = last
            return True
        else:
            return False
            
            
        
