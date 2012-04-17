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
                count_matrix[key] = count_matrix[key] + 1.
            else:
                count_matrix[key] = 1.

    tags = {}
    matrix_with_unknown = {}
    min_count = min(count_matrix.values())
    UNK = "UNK"
    for (k,v) in count_matrix.items():
        word = k.split()[0]
        tag = k.split()[1]
        if v == min_count:
            if matrix_with_unknown.has_key(UNK):
                if matrix_with_unknown[UNK].has_key(tag):
                    matrix_with_unknown[UNK][tag] += v
                else:
                    matrix_with_unknown[UNK][tag] = v
            else:
                matrix_with_unknown[UNK] = {}
                matrix_with_unknown[UNK][tag] = v
        else:
            if not matrix_with_unknown.has_key(word):
                matrix_with_unknown[word] = {}
            matrix_with_unknown[word][tag] = v
        if tags.has_key(tag):
            tags[tag] =  tags[tag] + 1.
        else:
            tags[tag] = 1.

    tag_size = float(len(tags))
    for (word,tag_dict) in matrix_with_unknown.items():
        for (tag, v) in tag_dict.items():
            matrix_with_unknown[word][tag] = (tag_dict[tag] + 1.) / (tags[tag] + tag_size)

    import math
    for (w,tag_dict) in matrix_with_unknown.items():
        for (tag, prob) in tag_dict.items():
            matrix_with_unknown[w][tag] = math.log((matrix_with_unknown[w][tag] + 1.) / (tag_size + tags[tag]))
        matrix_with_unknown[w]["SMOOTH"] = math.log(1. / tag_size)

    return (matrix_with_unknown, tags)

def get_tag_n_gram(n, filename, tags, bi):
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
                    count_matrix[k] = count_matrix[k] + 1.
                else:
                    count_matrix[k] = 1.

                # Get rid of last one.
                queue.pop()

    import copy
    counts = copy.deepcopy(count_matrix)

    import math
    if n==1:
        tot = sum(count_matrix.values())
        for (k,v) in count_matrix.items():
            count_matrix[k] = math.log(count_matrix[k] / tot) 
    elif n==2:
        tag_size = float(len(tags))
        for (k,v) in count_matrix.items():
            tag = k.split()[1] 
            count_matrix[k] = math.log((count_matrix[k] + 1.) / (tag_size + tags[tag]))
        count_matrix["SMOOTH"] = math.log(1. / tag_size)
    elif n>2:
        tag_size = float(len(tags))
        tagtag_size = tag_size
        for i in xrange(1,n):
            tagtag_size = tagtag_size * tag_size 
        for (k,v) in count_matrix.items():
            tagtag = " ".join(k.split()[1::])
            if bi.has_key(tagtag):
                tagval = bi[tagtag]
            else:
                tagval = 0.
            count_matrix[k] = math.log((count_matrix[k] + 1.) / (tagtag_size + tagval))
        count_matrix["SMOOTH"] = math.log(1. / tagtag_size)

    return (count_matrix, counts)


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

    word_tag_output = "tag_word_count2.json"
    tags_output = "tags2.json"
    bigram_matrix_name = "bigram_count2.json"
    unigram_matrix_name = "unigram_count2.json"
    trigram_matrix_name = "trigram_count2.json"

    sub_dir = os.path.join(output_dir, "count_matrix2/")
    if not os.path.exists(sub_dir):
        os.mkdir(sub_dir)

    (word_tag_matrix, tags) = get_tag_word_matrix(filename)
    with open(sub_dir + word_tag_output, "w") as f:
        json.dump(word_tag_matrix, f)
    with open(sub_dir + tags_output, "w") as f:
        json.dump(tags, f)

    (unigram_matrix, unigrams) = get_tag_n_gram(n=1, filename=filename, tags=None, bi=None)
    with open(sub_dir + unigram_matrix_name, "w") as f:
        json.dump(unigram_matrix, f)

    (bigram_matrix, bigrams) = get_tag_n_gram(n=2, filename=filename, tags=tags, bi=None)
    with open(sub_dir + bigram_matrix_name, "w") as f:
        json.dump(bigram_matrix, f)

    (trigram_matrix, trigrams) = get_tag_n_gram(n=3, filename=filename, tags=tags, bi=bigrams)
    with open(sub_dir + trigram_matrix_name, "w") as f:
        json.dump(trigram_matrix, f)

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

if __name__=="__main__":
    import sys
    #lemmatize_observation(sys.argv[1], sys.argv[2])
    create_count_matrix(sys.argv[1], sys.argv[2])
