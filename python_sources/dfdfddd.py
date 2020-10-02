
import random
from collections import defaultdict
import time

k = 100
len_t = 10**5
AGCT = "AGCT"
genome = "".join(random.choice(AGCT) for __ in range(len_t))
mygenome = list(genome)

board = ["_"] * len(genome)

for i in random.sample(range(len(genome)), len(genome)//1000):
    gen = t = mygenome[i]
    while gen == t:
        gen = random.choice("AGCT")
        mygenome[i] = gen
mygenome = "".join(mygenome)

numOfReads = 3000
read_length_range = (3*k,4*k)
reads = list()

for __ in range(numOfReads):
    r_l = random.randrange(k,2*k)
    r_i = random.randrange(len(mygenome)-r_l)
    reads.append(mygenome[r_i:r_i+r_l])

start_time = time.time()

def write_on_buffer(p, i, buffer = board):
    for j in range(len(p)):
        if board[i+j] == '_':
            board[i+j] = p[j]



class Index(object):

    def __init__(self, t, k):
        self.k = k  # k-mer length (k)
        self.index = defaultdict(list)
        for i in range(len(t) - k + 1):  # for each k-mer
            self.index[t[i:i+k]].append(i)  # add (k-mer, offset) pair

    def query(self, p_kmer):
        return self.index[p_kmer]

genome_k_mer_index = Index(genome,k)

def get_kmers(s,k):
    return [(j,s[j:j+k]) for j in range(len(s) - k + 1)]

for read in reads:
    hit_candidate = []
    for j, kmer in get_kmers(read,k):
        for i in genome_k_mer_index.query(kmer):
            write_on_buffer(read, i - j)


reconstructed = "".join(board)
print(reconstructed)

def hamming(x,y):
    s = 0
    for i,x in enumerate(zip(x,y)):
        a,b = x
        if a != b:
            s += 1
            #print(i, a, b)
    return s
    
print("hamming distance :",hamming(reconstructed,mygenome))
print("running_time :", time.time() - start_time)
max(len(x) for _, x in genome_k_mer_index.index.items())