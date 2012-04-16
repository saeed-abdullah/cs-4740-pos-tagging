from collections import Mapping

class ProbabilityDistribution(Mapping):

    def __init__(self, conditioned_count, tag_count, vocab_count):
        self._conditioned_count = conditioned_count
        self._tag_count = tag_count
        self._vocab_count = vocab_count

    def __iter__(self):
        return self._tag_count.__iter__()

    def __len__(self):
        return self._tag_count.__len__()

    def __getitem__(self, key):
        word = key.split()[0]
        tag = key.split()[1]
        if not self._conditioned_count.has_key(key):
            unk_tag = "UNK " + tag
            if self._vocab_count.has_key(word):
                return 0.
            elif self._conditioned_count.has_key(unk_tag):
                conditioned_count = self._conditioned_count[unk_tag]
            else:
                return 0.
        else:
            conditioned_count = self._conditioned_count[key]

        return float(conditioned_count)/self._tag_count[tag]

class SmoothedDistribution(ProbabilityDistribution):
    def __init__(self, conditioned_count, tag_count, vocab_count):
        super(SmoothedDistribution, self).__init__(
                conditioned_count, tag_count, vocab_count)

    def __getitem__(self, key):
        word = key.split()[0]
        tag = key.split()[1]
        if not self._conditioned_count.has_key(key):
            unk_tag = "UNK " + tag
            if self._vocab_count.has_key(word):
                r = 0
            elif self._conditioned_count.has_key(unk_tag):
                r = self._conditioned_count[unk_tag]
            else:
                r = 0
        else:
            r = self._conditioned_count[key]

        return float(r + 1)/(self._tag_count[tag] + 
                len(self._tag_count.keys()))

