import sys, os, operator

def main(argv):
    pattern_template = "patterns/pattern-%i.txt"
    output_template = "max/max-%i.txt"

    for i in range(5):
        patterns = [{}, {}, {}] 
        max_patterns = {} 

        # read in mined frequent patterns and divide by number of terms
        with open(pattern_template % i, 'r') as data:
            for line in data.readlines():
                data_line = line.rstrip().split(" ")
               
                if len(data_line) == 2:
                    patterns[0][(data_line[1],)] = data_line[0]
                elif len(data_line) == 3:
                    patterns[1][tuple(data_line[1:])] = data_line[0]
                elif len(data_line) == 4:
                    patterns[2][tuple(data_line[1:])] = data_line[0]

        # check terms of size 1 or 2
        for j in range(1):
            for pattern in patterns[j]:
                confirmed = False

                for next_p in patterns[j + 1]:
                    flag = True

                    # check for superset that contains same terms
                    # if it exists, do not add to max pattern list
                    for term in pattern:
                        if term not in next_p:
                            flag = False
                            break

                    if flag:
                        confirmed = True
                        break

                if not confirmed:
                    max_patterns[pattern] = int(patterns[j][pattern])

        # sort by support in descending order and write out max patterns
        max_sorted = sorted(max_patterns.items(), key = operator.itemgetter(1))

        if os.path.isfile(output_template % i):
            os.remove(output_template % i)

        with open(output_template % i, 'w') as out_file:
            for pattern in reversed(max_sorted):
                out_file.write(str(pattern[1]))

                for term in pattern[0]:
                    out_file.write(" %s" % term)
                
                out_file.write("\n")


if __name__ == "__main__":
    main(sys.argv)

