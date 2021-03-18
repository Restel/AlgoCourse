import random
import sys
import numpy as np
import time
#start = time.time()
str = sys.stdin.readline()
N, M, mod = str.split(" ")
N = int(N)
M = int(M)
mod = int(mod)

def read_seq():
    a = [0]
    temp = sys.stdin.readline().split("\n")[0]
    temp = temp.strip()
    temp = temp.split(" ")
    temp = [int(elem) for elem in temp]
    a.extend(temp)
    return a

a_seq = read_seq()
b_seq = read_seq()
S = np.ones((N + 1, M + 1), dtype=np.int)
for i in range(1, N + 1):
    for j in range(1, M + 1):
        if a_seq[i] == b_seq[j]:
            S[i,j] = (2 * S[i-1, j-1]) % mod
        else:
            S[i, j] = (S[i - 1, j] + S[i, j - 1] - S[i - 1, j - 1]) % mod

def sampling_seq(S, a, b, M, N):
    com_seq = []
    r = random.random() # a random number in (0,1]
    while S[N,M] != 1:
        if a[N] == b[M]:
            if r < S[N-1, M-1]/S[N,M]:
                com_seq.append(a[N])
            M -= 1
            N -= 1
        else:
            prob_i = (S[N,M]- S[N-1,M])/S[N,M]
            prob_j = (S[N,M]- S[N,M-1])/S[N,M]
            prob_None = S[N-1, M-1]/S[N,M]
            prob = [prob_i, prob_j, prob_None]
            prob_norm = []
            for z in range(1,4):
                prob_norm.append(sum(prob[0:z]))
            if r >= 0 and r < prob_norm[0]:
                com_seq.append(a[N])
                N -= 1
            elif r >=prob_norm[0] and r < prob_norm[1]:
                com_seq.append(b[M])
                M -= 1
            else:
                N -= 1
                M -= 1
    com_seq.reverse()
    return com_seq


print(sampling_seq(S, a_seq, b_seq, M, N))