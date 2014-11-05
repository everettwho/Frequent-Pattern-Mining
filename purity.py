import sys, os, operator
from math import log

def main(argv):
    pattern_template = "patterns/pattern-%i.txt"
    topic_template = "data-assign3/topic-%i.txt"
    output_template = "purity/purity-%i.txt"
    vocab = {}
    patterns = []
    topic_data = []
    Dt_values = [10047, 9674, 9959, 10161, 9845]
    Dtt_values = [[0, 17326, 17988, 17999, 17820],
                  [17326, 0, 17446, 17902, 17486],
                  [17988, 17466, 0, 18077, 17492],
                  [17999, 17902, 18077, 0, 17912],
                  [17820, 17486, 17492, 17912, 0]]

    # read all values for patterns, topics, and vocab into respective lists
    for i in range(5):
        with open(pattern_template % i, 'r') as data:
            patterns.append({})
            
            for line in data.readlines():
                split_data = line.rstrip().split(' ') 
                patterns[i][split_data[1]] = split_data[0]
        
        with open(topic_template % i, 'r') as data:
            topic_data.append([])

            for line in data.readlines():
                topic_data[i].append(tuple(line.rstrip().split(' '))) 

        with open("data-assign3/vocab.txt", 'r') as data:

            for line in data.readlines():
                vocab_data = line.rstrip().split("\t")
                vocab[vocab_data[1]] = vocab_data[0]

    # run purity calculations for every pattern-i.txt file
    for i in range(5):
        purity_values = {}

        # iterate over each frequent pattern in the file
        for pattern in patterns[i]:
            temp = []
            f_tp = float(patterns[i][pattern])

            for j in range(5):
                if i != j:
                    # check for frequency of pattern in other pattern-j.txt file
                    # if it exists, use this value, otherwise get value from topic-j.txt file
                    if pattern in patterns[j]:
                        temp.append((f_tp + float(patterns[j][pattern])) / Dtt_values[i][j])
                    else:
                        count = 0
                        terms = pattern.split(" ")

                        # count frequency of pattern in topic data
                        for data in topic_data[j]:
                            flag = True

                            for term in terms:
                                term_num = vocab[term]

                                if term_num not in data:
                                    flag = False

                            if flag:
                                count += 1

                        if count != 0:
                            temp.append((f_tp + count) / Dtt_values[i][j])

            # calculate purity based on maximum value in temp
            if temp:
                purity_values[pattern] = log(f_tp / Dt_values[i], 10) - log(max(temp), 10)
            else:
                purity_values[pattern] = log(f_tp / Dt_values[i], 10) 

        sorted_by_purity = []

        for pattern in purity_values:
            sorted_by_purity.append((purity_values[pattern], pattern, patterns[i][pattern]))

        # sort values first on purity, and if there is a tie, then on support values
        sorted_by_purity = sorted(sorted_by_purity, key = operator.itemgetter(0, 2))

        if os.path.isfile(output_template % i):
            os.remove(output_template % i)

        # write data in descending order of purity and support
        with open(output_template % i, 'w') as out_file:
            for data in reversed(sorted_by_purity):
                out_file.write("%f %s\n" % (data[0], data[1]))

if __name__ == "__main__":
    main(sys.argv)

