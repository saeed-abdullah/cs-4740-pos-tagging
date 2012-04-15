from collections import Mapping

class ProbabilityDistribution(Mapping):

    def __init__(self, conditioned_count, tag_count):
        self._conditioned_count = conditioned_count
        self._tag_count = tag_count

    def __iter__(self):
        return self._tag_count.__iter__()

    def __len__(self):
        return self._tag_count.__len__()

    def __getitem__(self, key):
        if not self._conditioned_count.has_key(key):
            return 0.

        conditioned_count = self._conditioned_count[key]
        tag = key.split()[1]

        return float(conditioned_count)/self._tag_count[tag]

class SmoothedDistribution(ProbabilityDistribution):
    def __init__(self, conditioned_count, tag_count):
        super(SmoothedDistribution, self).__init__(
                conditioned_count, tag_count)

    def __getitem__(self, key):
        if not self._conditioned_count.has_key(key):
            r = 0
        else:
            r = self._conditioned_count[key]

        tag = key.split()[1]
        return float(r + 1)/(self._tag_count[tag] + 
                len(self._tag_count.keys()))

"""
class TrigramDistribution(Mapping):
    def __init__(self, trigram_count, bigram_count, unigram_count):
        self._trigram_count = trigram_count
        self._bigram_count = bigram_count
        self._unigram_count = unigram_count
        self._total_count = sum(self._unigram_values())
        self._update_params()

    def _deleted_interpolation(self):

        lambda_1 = 0.
        lambda_2 = 0.
        lambda_3 = 0.

        for trigram in self._trigram_count.keys():

            grams = trigram.split()

            nominator = self._trigram_count[trigram] - 1
            denominator =  self._bigram_count[" ".join(grams[:-1])] - 1
            p1 = float(nominator)/denominator

            nominator = self._bigram_count[" ".join(grams[1:])] - 1
            denominator = self._unigram_count[grams[1]] - 1
            p2 = float(nominator)/denominator

            nominator = self._unigram_count[grams[2]] - 1
            denominator = self._total_count - 1
            p3 = float(nominator)/denominator

            m = max([p1, p2, p3])
            if m == p1:
                lambda_1 += self.



"""
