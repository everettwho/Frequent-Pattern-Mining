import sys, os, operator
from optparse import OptionParser
from itertools import chain, combinations

class Apriori(object):
    def __init__(self, items, min_sup, output_file):
        self.all_items = items
        self.min_freq = min_sup * len(items)
        self.out_file = output_file 

    def run_apriori(self):
        mined_patterns = {}
        size = 2
        candidates = self._get_initial_candidates()
        frequent = {key: value for (key, value) in self._get_next_frequent(candidates)}

        # add current frequent itemsets of size 1 to mined patterns
        mined_patterns.update(frequent)

        # continue running until no frequent itemsets can be created
        while frequent:
            # retrieve candidates and frequent patterns based on those candidates
            candidates = self._get_next_candidates(frequent, size)
            frequent = {key: value for (key, value) in self._get_next_frequent(candidates)}

            # add frequent patterns to mined patterns dictionary
            mined_patterns.update(frequent)
            size += 1

        sorted_by_support = sorted(mined_patterns.items(), key = operator.itemgetter(1))

        self._write_output(sorted_by_support) 

    def _write_output(self, patterns):
        vocab_file = open("data-assign3/vocab.txt", 'r')
        vocab = {}

        for line in vocab_file.readlines():
            data = line.rstrip().split("\t")
            vocab[data[0]] = data[1]

        if os.path.isfile(self.out_file):
            os.remove(self.out_file)

        # pattern dictionary is reversed and written to file in order of descending support
        with open(self.out_file, 'w') as out_file:
            for pattern in reversed(patterns):
                out_file.write(str(pattern[1]))

                if isinstance(pattern[0], tuple):
                    for term in pattern[0]:
                        out_file.write(" " + str(vocab[term]))
                else:
                    out_file.write(" " + str(vocab[pattern[0]]))

                out_file.write("\n")

    def _generate_candidates(self, item_set, size):
        if size == 2:
            # no need to check subsets for first iteration
            return list(combinations(set(chain(item_set.keys())), size))
        else:
            possible = list(combinations(set(chain.from_iterable(item_set.keys())), size))
            confirmed = []

            for combination in possible:
                subsets = list(combinations(chain(combination), size - 1))
                flag = True
                    
                # check for subsets in previous frequent pattern list
                for subset in subsets:
                    if subset not in item_set:
                        flag = False

                # return only those itemsets which have all possible 
                # subsets in previous frequent pattern list
                if flag:
                    confirmed.append(combination)

            return confirmed
                

    def _get_initial_candidates(self):
        item_set = {}

        # create dictionary of all individual terms as keys and counts as values
        for item in self.all_items:
            for term in item:
                if term not in item_set:
                    item_set[term] = 1;
                else:
                    item_set[term] += 1;

        return item_set

    def _get_next_candidates(self, last_frequent, size):
        candidates = {}
        sets = self._generate_candidates(last_frequent, size)

        # get count for all possible candidates
        for candidate_set in sets:
            for item in self.all_items:
                flag = True

                for value in candidate_set:
                    if value not in item:
                       flag = False
                       break

                if flag:
                    if candidate_set in candidates:
                        candidates[candidate_set] += 1
                    else:
                        candidates[candidate_set] = 1

        return candidates

    def _get_next_frequent(self, current_candidates):
        # generator function yields terms with count higher than threshold
        for candidate in current_candidates:
            if current_candidates[candidate] >= self.min_freq:
                yield(candidate, current_candidates[candidate])

def main(argv):
    parser = OptionParser()

    parser.add_option('--dataFile',
                      dest = 'data_file_name', 
                      help = 'data file name',
                      default = None)

    parser.add_option('--outputFile',
                      dest = 'output_file_name',
                      help = 'output file name',
                      default = None)

    parser.add_option('--minSup',
                      dest = 'min_sup',
                      help = 'minimum support value',
                      default = 0.004)

    (opts, args) = parser.parse_args()

    if opts.data_file_name is None:
        print "Data file name required"
        sys.exit(-1)

    if opts.output_file_name is None:
        print "Output file name required"
        sys.exit(-1)

    items = []  

    with open(opts.data_file_name, 'r') as data_file:
        for line in data_file.readlines():
            items.append(tuple(line.rstrip().split(' ')))


    apriori = Apriori(items, opts.min_sup, opts.output_file_name)
    apriori.run_apriori()
    
if __name__ == "__main__":
    main(sys.argv[1:])
