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
print(S[N, M])
