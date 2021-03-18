import sys
import numpy as np
import time
# for i in range(5):
# todo include loop for all input, output the solution, estimate time
start = time.time()
str = sys.stdin.readline()
N, W, mod = str.split(" ")
N = int(N)
W = int(W)
mod = int(mod)
weight = [0]
for i in range(N):
    weight.append(int(sys.stdin.readline()))

S = np.zeros((W + 1, N + 1), dtype=np.object)
for v in range(1, W + 1):
    for k in range(1, N + 1):
        if weight[k] <= v:
            S[v, k] = (sum(S[v-weight[k],1:k]) + 1) % mod
answer = sum(S[W, :]) + 1
answer = answer % mod
print(answer, time.time() - start)

