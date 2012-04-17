from collections import Mapping

class SmoothedDistribution(Mapping):
    def __init__(self, conditioned_count, tag_count):
        self._conditioned_count = conditioned_count
        self._tag_count = tag_count

    def __iter__(self):
        return self._tag_count.__iter__()

    def __len__(self):
        return self._tag_count.__len__()

    def __getitem__(self, key):
        #observation table
        if self._conditioned_count.has_key("UNK"):
            w_t = key.split()
            if self._conditioned_count.has_key(w_t[0]):
                if self._conditioned_count[w_t[0]].has_key(w_t[1]):
                    return self._conditioned_count[w_t[0]][w_t[1]]
                return self._conditioned_count[w_t[0]]["SMOOTH"]
            else:
                if self._conditioned_count["UNK"].has_key(w_t[1]):
                    return self._conditioned_count["UNK"][w_t[1]]
                return self._conditioned_count["UNK"]["SMOOTH"]
        #transition matrices
        if self._conditioned_count.has_key(key):
            return self._conditioned_count[key]
        return self._conditioned_count["SMOOTH"]
