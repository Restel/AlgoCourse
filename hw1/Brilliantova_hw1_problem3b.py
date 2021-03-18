import sys
import numpy as np
import random
import matplotlib.pyplot as plt
str = sys.stdin.readline()
N, W, mod = str.split(" ")
N = int(N)
W = int(W)
# mod = int(mod)
weight = [0]
for i in range(N):
    weight.append(int(sys.stdin.readline()))

S = np.zeros((W + 1, N + 1), dtype=np.object)
for v in range(1, W + 1):
    for k in range(1, N + 1):
        if weight[k] <= v:
            S[v, k] = sum(S[v-weight[k], 1:k]) + 1

prob_N = S[W, N]/sum(S[W, :(N+1)])
# print(prob_N)

def one_sample(prints):
    hit = False
    i = N
    Z = W
    sample = []
    while i > 0:
        total = sum(S[Z, :(i+1)]) + 1
        rand = random.random()
        if rand < (S[Z, i] / total):
            Z -= weight[i]
            sample.append(i)
            if i == N:
                hit = True
        i -= 1
    if prints:
        print(*sample)
    return hit

def estimate_prob(sample_rep):
    hits = 0
    for i in range(sample_rep):
        if one_sample():
            hits += 1
    return(hits/sample_rep)

results = np.zeros(7)

one_sample(True)

# N_samples = []
# for i in range(0, 7):
#     sample_rep = 10 ** i
#     N_samples.append(i)
#     results[i] = estimate_prob(sample_rep)

# plt.plot(N_samples, results)
# plt.xlabel('Number of samples, log10 scale')
# plt.ylabel('Rk')
# plt.show()

