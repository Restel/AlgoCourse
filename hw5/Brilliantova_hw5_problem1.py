import random
import sys
import numpy as np
import time
import math

# start = time.time()
def read_input():
    str = sys.stdin.readline()
    N, M = str.split(" ")
    N = int(N)
    M = int(M)

    def read_edge():
        temp = sys.stdin.readline().split("\n")[0]
        temp = temp.strip()
        temp = temp.split(" ")
        temp = [int(elem) for elem in temp]
        return temp

    E = [None]
    for i in range(M):
        edge = read_edge()
        E.append(edge)

    print(E)
    return N,M,E


def MC_step(M, E, test = False, edge = 1):
    """Make a single Markov chain MC step by trnaforming given state M. Choose a random edge ei from E. If ei = (ai,bi) do not belong to M and can be added (i.e. there is no edges incident to ai and bi), than the function adds it to M. If (ai, bi) belong to M, it removes it from M
    :param M: a current state (valid matching)
    :param E: list of edges
    :pre: E includes a dummy edge at 0 index
    :pre: M includes a dummy vertex at row 0
    :pre: M[:,0] is a sum of degrees of each vertex.
    :return: M, a next state in the chain
    """
    m = len(E)
    if not test:
        x = random.randint(1, m-1) # choose a random edge
    else:
        x = edge

    a,b = E[x] # vertices connected by the chosen edge

    # test if an edge is not mutal
    if (M[a,b] == 1 and M[b,a] != 1) or (M[a,b] != 1 and M[b,a] == 1):
        raise ValueError("A unidirected edge is found: [", a, b, "]")

    # if the chosen edge x already exists, delete x
    if M[a,b] == 1 and M[b,a] == 1:
        M[a,b] = 0
        M[b,a] = 0
        M[a,0] -= 1
        M[b,0] -= 1

    # if there are no edges incident to a and b include edge x
    elif M[a,0] == 0 and M[b,0] == 0:
        M[a,b] = 1
        M[b,a] = 1
        M[a,0] += 1
        M[b,0] += 1

    return x,M

def MC_steps(steps, E, m, n):
    """Perform the desired number of MC steps starting from an empty matching. On each step call MC_step subroutine"""

    matching = np.zeros((n+1, m+1), dtype=int)
    for i in range(steps):
        e, matching = MC_step(matching, E)
        #print("after choosing e", E[e], " matching is", matching)
    return matching

def validate_matching(M, removed_edge):
    """Indicator function representing if matching M is a valid matching for G \ {e}"""
    matched_edges = np.argwhere(M == 1)
    for elem in matched_edges:
        set_edge = set(elem)
        if set_edge == removed_edge:
            return 0
    return 1

def test_FPAUS():
    E = [None, [1,2], [2,3], [2,4], [3,4], [3,5], [4,5]]
    n = 5
    m = 6
    M = np.zeros((n+1, m+1), dtype=int)
    M[1,2] = 1
    M[1,0] = 1
    M[2,0] = 1
    M[2,1] = 1
    print("Current Matching", M)
    _, M = MC_step(M, E, test=True, edge = 1)
    print("After deleting edge = (1,2): ", M)
    _, M = MC_step(M, E, test=True, edge = 6)
    print("After adding edge = (4,5):", M)
    _, M = MC_step(M, E, test=True, edge=4)
    print("After adding edge = (3,4):", M)
    _, M = MC_step(M, E, test=True, edge=2)
    print("After adding edge = (2,3):", M)

def calculate_mixing_time(n, m, eps):
    """Given number of edges and vertices and the counting error, calculate the mixing time for matching markov chain """
    d = eps / (6 * m)
    time = n * m * (4 * math.log(1/d) + 2 * n * math.log(n) + n * abs(math.log(1)))
    return time

def count_MC(eps = 0.1):
    n, m, E = read_input()
    s = int(75 * m /(eps ** 2))  # number of samples in counting
    Z_bar = []
    E_i = E.copy()
    for i in range(m, 1, -1):
        e_list = E_i[i] # an edge to be removed
        e = set(e_list)
        Z = []
        mix_time = int(calculate_mixing_time(n, i, eps))
        for j in range(s):
            M_i = MC_steps(mix_time, E_i, m, n)
            Z_j = validate_matching(M_i, e) # check if M_i is valid when e is removed
            Z.append(Z_j)
            print(i, j)
        Z_bar.append(sum(Z)/len(Z))
        E_i.remove(e_list) # remove an edge
    product = np.prod(Z_bar) # multiple the ratios
    return 1/product

def main_test():
    print("============Test 1===========")
    E = [None, [1,2], [2,3], [2,4], [3,4], [3,5], [3,2]]
    n = 5
    m = 6
    matching = MC_steps(1, E, m, n)
    print(matching)
    print("============Test 2===========")
    test_FPAUS()
    # print("============Test 3===========")
    # n, m, E = read_input()
    # MC_steps(10, E, m, n)
    print("============Test 4===========")
    num_matchings = count_MC()
    print(num_matchings)

def main():
    num_matchings = count_MC()
    print(num_matchings)

main()