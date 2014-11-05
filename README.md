Frequent-Pattern-Mining
=======================

Frequent pattern mining application on text mining to discover meaningful phrases.

LDA is run on a data set made up of titles from 5 domains' conference papers.  Using the results of the LDA, a topic is assigned to each word of each title.  Each topic represents one of five domains in computer science: Data Mining (DM), Machine Learning (ML), Database (DB), Information Retrieval (IR), Theory (TH). Each file in the data-assign3/ folder represents a topic in which each line contains words assigned to that topic.  

A basic Apriori algorithm is implemented in apriori.py which takes and input file, output file, and support level.  This algorithm generates frequent patterns that meet the support level based on the algorithm.  The output of running this algorithm on each topic can be found in the patterns/ folder.

Maximal and closed patterns are then mined using max.py and closed.py, with outputs in max/ and closed/, respectively.

The purity of each pattern in the patterns/ folder is ranked by purity, which is measrued by comparing the probability of seeing a phrase in the topic-t collection D(t) and the probability of seeing it any other topic-t' collection. This is calculated according to the following equation:

purity(p,t)=log [ f(t,p) / | D(t) | ] - log (max [ ( f(t,p) + f(t',p) ) / | D(t,t') | ] )

t' is in the set {0, 1, ..., k} where k is the number of topics - 1 (in this case k = 4), t' represents any other topic collection, 
purity(p,t) is the purity of pattern 'p' in topic 't', 
f(t,p) is the frequency of pattern 'p' in topic 't', 
D(t) is the set defined as {d | topic 't' is assigned to at least one word in document 'd'}
D(t,t') is the union of D(t) and D(t')

In this particular case, the value |D(t)| is represented by the number of lines in each topic file due to preprocessing.

The purity rankings can be found in the purity/ folder.
