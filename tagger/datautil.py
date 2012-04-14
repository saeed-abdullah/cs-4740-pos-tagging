# Utility for data handling.

def get_tag_word_matrix(filename):
    """Returns count matrix for tag-word pair.

    params
    ----
    filename: Path of input file.

    returns
    ----
    A dictionary where key is a line from file. So, for given POS train data
    each key is a sequence of tag and word seperated by a space.
    """

    count_matrix = {}
    with open(filename) as f:
        for l in f:
            line = l.strip()
            if not line:
                continue

            if line not in count_matrix.keys():
                count_matrix[line] = 1
            else:
                count_matrix[line] += 1

    return count_matrix

def get_tag_n_gram(n, filename):
    """Returns a count matrix for N gram.

    param
    ----
    n: Length of conditioning sequence.
    filename: Input file path

    reutrn
    ----
    A dictionary with key as the N grams seperated by space. For example,
    given for tag sequcne "NNP NP VP" the bigram dictionary would contain
    'NP NNP', 'VP NP' as keys.
    """

    from collections import deque
    queue = deque()

    count_matrix = {}
    with open(filename) as f:
        for l in f:
            line = l.strip().split()
            if not line:
                continue

            tag = line[0]
            # Use a queue to keep track of conditioned string,
            # the occurence of last N - 1 string.
            queue.appendleft(tag)

            # Fill the queue until it gets at least N tags.
            if len(queue) > n - 1:
                k = " ".join(queue)
                if k not in count_matrix.keys():
                    count_matrix[k] = 1
                else:
                    count_matrix[k] += 1

                # Get rid of last one.
                queue.pop()

    return count_matrix

