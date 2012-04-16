# Utility for data handling.

def get_tag_word_matrix(filename):
    """Returns count matrix for tag-word pair.

    params
    ----
    filename: Path of input file.

    returns
    ----
    A dictionary where key is contains word and tag seperated by space.
    """

    count_matrix = {}
    with open(filename) as f:
        for l in f:
            line = l.strip()
            if not line:
                continue

            # Reversing the position of word and tag
            key = " ".join(line.split()[::-1])
            if count_matrix.has_key(key):
                count_matrix[key] += 1
            else:
                count_matrix[key] = 1

    matrix_with_unknown = {}
    vocab_dict = {}
    min_count = min(count_matrix.values())
    for (k,v) in count_matrix.items():
        if v == min_count:
            tag = k.split()[1]
            unk_tag = "UNK " + tag
            if matrix_with_unknown.has_key(unk_tag):
                matrix_with_unknown[unk_tag] += v
            else:
                matrix_with_unknown[unk_tag] = v
        else:
            matrix_with_unknown[k] = v
            word = k.split()[0]
            vocab_dict[word] = 1

    return (matrix_with_unknown, vocab_dict)

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
                if count_matrix.has_key(k):
                    count_matrix[k] += 1
                else:
                    count_matrix[k] = 1

                # Get rid of last one.
                queue.pop()

    return count_matrix


def create_count_matrix(filename, output_dir):
    """Creates count matrix from the training file.

    It reads the training file and saves the count matrices for
    unigram, bigram, trigram and tag-word in the count_matrix/
    sub-directory created in the given output_dir.

    param
    ----
    filename: Path of training file.
    output_dir: Output directory.
    """

    import os
    import json

    word_tag_output = "tag_word_count.json"
    vocab_output = "vocab_dict.json"
    bigram_matrix_name = "bigram_count.json"
    unigram_matrix_name = "unigram_count.json"
    trigram_matrix_name = "trigram_count.json"

    sub_dir = os.path.join(output_dir, "count_matrix/")
    if not os.path.exists(sub_dir):
        os.mkdir(sub_dir)

    (word_tag_matrix, vocab_dict) = get_tag_word_matrix(filename)
    with open(sub_dir + word_tag_output, "w") as f:
        json.dump(word_tag_matrix, f)
    with open(sub_dir + vocab_output, "w") as f:
        json.dump(vocab_dict, f)

    unigram_matrix = get_tag_n_gram(n=1, filename=filename)
    with open(sub_dir + unigram_matrix_name, "w") as f:
        json.dump(unigram_matrix, f)

    bigram_matrix = get_tag_n_gram(n=2, filename=filename)
    with open(sub_dir + bigram_matrix_name, "w") as f:
        json.dump(bigram_matrix, f)

    trigram_matrix = get_tag_n_gram(n=3, filename=filename)
    with open(sub_dir + trigram_matrix_name, "w") as f:
        json.dump(trigram_matrix, f)


if __name__=="__main__":
    import sys

    create_count_matrix(sys.argv[1], sys.argv[2])
