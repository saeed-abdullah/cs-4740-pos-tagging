class DynamicTable:

    def __init__(self):
        """
        initializes internal data structures for viterbi representation
        """

    def prob(self, m, n):
        """
        Returns the probability of the path of predictions ending in
        last(m, n)
        ----
        input
            m:  row index to be queried
            n:  column index to be queried
        """

    def last(self, m ,n):
        """
        Returns the last word in the sequence that produced
        the probability stored at prob(m, n)
        ----
        input
            m:  row index to be queried
            n:  column index to be queried
        """

    def full_path(self, m, n):
        """
        Returns the full path that produces the probability given at
        prob(m, n)
        ----
        input
            m:  row index to be queried
            n:  column index to be queried
        """

    def update(self, col):
        """
        Updates internal data structures by adding a column that represents
        one step of a Viterbi algorithm's computations.
        ----
        input
            col:  full column of output from a Viterbi algorithm.  Must agree
                  in size with current data structures.

        returns True if colums is properly sized, False otherwise
        """
