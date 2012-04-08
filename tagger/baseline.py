# Basesline tagger which uses most frequent pos for a word.

def parse_train_data(filename):
    """Parses train data to build tag list for words.

    param
    ----
    filename: Path of train file.

    returns
    ----
    It returns two-level dictionary where the first level is keyed by the
    word and the second level is keyed by the tags. For example, see
    BaselineTest._tags attribute.
    """

    tags = {}
    with open(filename) as f:
        for line in f:
            l = line.strip().split()
            w = l[1]
            t = l[0]

            if w not in tags.keys():
                # Initiate a new dictionary for w
                tags[w] = {t:1}
            else:
                # Word has been seen before but not for
                # this tag.
                if t not in tags[w].keys():
                    tags[w][t] = 1
                else:
                    tags[w][t] += 1

    return tags

def get_baseline_tags(tags):
    """Returns the most used tags for each word.

    params
    ----
    tags: A two level dictionary as created in parse_train_data.

    returns
    ----
    A tuple of most used tag overall and a dictionary which contains most
    used tag for particular word.
    """

    tag_count = {}
    word_tagged = {}

    for w, t in tags.iteritems():
        sorted_tags = sorted(t, key=lambda key: t[key], reverse=True)
        most_frequent_tag = sorted_tags[0]

        word_tagged[w] = most_frequent_tag
        if most_frequent_tag in tag_count.keys():
            tag_count[most_frequent_tag] += t[most_frequent_tag]
        else:
            tag_count[most_frequent_tag] = t[most_frequent_tag]

    default_tag = sorted(tag_count, key=lambda k: tag_count[k],
            reverse=True)[0]
    return default_tag, word_tagged

def write_test_tags(default_tag, tagged, lines, filename):
    """Writes output in kaggle format.
    params
    ----
    default_tag: Default tag to be used for unknown words.
    tagged: A dictionary containing word and corresponding tag.
    lines: A sequence of test lines.
    filename: Output file path.
    """

    line_template = "{0} {1}\n"
    with open(filename, "w") as fout:
        for l in lines:
            line = l.strip()
            if line not in tagged.keys():
                fout.write(line_template.format(default_tag, line))
            else:
                fout.write(line_template.format(tagged[line], line))


def main(trainfile, testfile, outputfile):
    tag_list = parse_train_data(trainfile)
    default, word_tagged = get_baseline_tags(tag_list)

    print default

    with open(testfile) as f:
        write_test_tags(default, word_tagged, f, outputfile)

if __name__ == "__main__":
    import sys
    main(sys.argv[1], sys.argv[2], sys.argv[3])
