__author__ = "Lina Brilliantova, RIT"
"""The program outputs the shortest sequence of words connecting two English words. Each word in the sequence is obtained by changing one letter or shifting letter to right. 
Usage: python3 wordseq.py [name of a dictionary] [word #1] [word #2] 
Example: 
>>> python3 wordseq.py words CHIP TOPS
>>> CHIP -> SHIP -> SHOP -> STOP -> TOPS """

#FIX if no connection can be made: print "No connection possible"

import sys
from queue import Queue
from string import ascii_uppercase

def load_words(filename):
    words_dict = {}
    with open(filename) as f:
        for line in f:
            word = line.upper().rstrip()
            words_dict[word] = word
    return words_dict

def insert_letter(word, letter, ind):
    if ind >= len(word):
        raise ValueError("Index of insertion must be less than the word length!")
    if ind == 0:
        before = ''
        after = word[ind+1:]
    elif ind == len(word) - 1:
        before = word[:ind]
        after = ''
    else:
        before = word[:ind]
        after = word[ind + 1:]
    return before + letter + after

def is_valid_successor(current, word_new, successors, words_dict):
    """Returns true if the word is not an already discovered successor, if it does not equal the orinigal word and if it is the list of valid English words"""
    return word_new not in successors and word_new != current and word_new in words_dict

def shift(word_ori, ind):
    l = len(word_ori)
    return word_ori[l-ind:] + word_ori[: l-ind]

def successors(node, words_dict):
    """Generates the successors of a given word"""
    successors = []
    # Change letters
    for i in range(len(node)):
        for letter in ascii_uppercase:
            word_new = insert_letter(node, letter, i)
            print(word_new)
            if is_valid_successor(node, word_new, successors, words_dict):
                successors.append(word_new)
    #Shift the word
    for i in range(1, len(node)):
        word_new = shift(node, i)
        if is_valid_successor(node, word_new, successors, words_dict):
            successors.append(word_new)
    return successors

def make_sequence(init, goal, parents):
    """Backtrack a path from init to goal using parents hash table"""
    seq = []
    seq.append(goal)
    current = goal
    parent = parents[current]
    seq.append(parent)
    while not parent == init:
        current = parent
        parent = parents[current]
        seq.append(parent)
    seq.reverse()
    return seq

def BFS(init, goal, words_dict):
    if len(init) != len(goal):
        exit("No sequence possible") # if the length of the words are different, there is no possible sequence, as insertion and shifting are lenght-preserving operations
    Q = Queue()
    parents = {}
    Q.put(init) # insert the initial word into the queue
    parents[init] = None
    while True:
        if Q.empty():
            exit("No sequence possible")
        current = Q.get()
        if current == goal:
            return make_sequence(init, current, parents)
        for s in successors(current, words_dict):
            if s not in parents:
                Q.put(s)
                parents[s] = current


def testing():
    print("=================================")
    print("=== TESTING SHIFT OPERATION =====")
    print(shift('ROTATE', 2))
    print("Should be: TEROTA")
    print(shift('ROTATE', 3))
    print("Should be: ATEROT")
    print(shift('ROTATE', 1))
    print("Should be: EROTAT")
    print(shift('ROTATE', 0))
    print("Should be: ROTATE")
    print(shift('ROTATE', len('ROTATE')))
    print("Should be: ROTATE")
    print("=================================")
    print("== TESTING INSERTION OPERATION ===")
    print(insert_letter('ROTATE', 'B', 0))
    print("Should be: BOTATE")
    print(insert_letter('ROTATE', 'U', len('ROTATE') - 1))
    print("Should be: ROTATU")
    print(insert_letter('ROTATE', 'Y', 3))
    print("Should be: ROTYTE")
    print(insert_letter('ICE', 'C', 1))
    # print(insert_letter('ROTATE', 'Y', 6))
    print(successors('CHIP', words_dict))
    print("=================================")
    print(is_valid_successor("CHIP", "CHIN", [], words_dict))
    print(BFS('CHIP', 'SHIP', words_dict))
    print(BFS('SHIP', 'CHIN', words_dict))

if __name__ == "__main__":
    filename = sys.argv[1]
    word_init = sys.argv[2].upper()
    word_goal = sys.argv[3].upper()
    words_dict = load_words(filename)
    print(BFS(word_init, word_goal, words_dict))
