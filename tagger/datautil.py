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
            if key not in count_matrix.keys():
                count_matrix[key] = 1
            else:
                count_matrix[key] += 1

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

def lemmatize_observation(fin, outputfile):
    """Lemmatizes the words.

    It uses wordnet lemmatizer from nltk. It is assumed that
    there is a local copy of nltk data available. For more details,
    see: http://nltk.googlecode.com/svn/trunk/doc/howto/data.html

    param
    ----
    fin: File like object which can be iterated for training or test lines.
    If the file contains more than one words per line (training data),
    then it will lemmatize the second word.

    outputfile: Output path.
    """

    import nltk
    lemmatizer = nltk.WordNetLemmatizer()
    
    with open(outputfile, "w") as fout:
        for l in fin:
            line = l.strip().split()
            if len(line) == 0:
                continue

            if len(line) == 1:
                # Test data
                line[0] = lemmatizer.lemmatize(line[0])
            else:
                # Training data
                line[1] = lemmatizer.lemmatize(line[1])

            fout.write(" ".join(line))
            fout.write("\n")


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
    bigram_matrix_name = "bigram_count.json"
    unigram_matrix_name = "unigram_count.json"
    trigram_matrix_name = "trigram_count.json"

    sub_dir = os.path.join(output_dir, "count_matrix/")
    if not os.path.exists(sub_dir):
        os.mkdir(sub_dir)

    word_tag_matrix = get_tag_word_matrix(filename)
    with open(sub_dir + word_tag_output, "w") as f:
        json.dump(word_tag_matrix, f)

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
