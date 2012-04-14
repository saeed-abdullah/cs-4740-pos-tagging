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

        if key not in self._conditioned_count.keys():
            return 0.

        conditioned_count = self._conditioned_count[key]
        tag = key.split()[0]

        return float(conditioned_count)/self._tag_count[tag]
