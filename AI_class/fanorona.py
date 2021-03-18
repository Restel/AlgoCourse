__author__ = 'Lina Brilliantova, RIT'
"""A program that plays the game fanorona. Implements   
Usage: python3 fanorona.py [X] [Y] [1 player] [2nd player] [depth_level_1] [depth_level_2]
Parameters: 
1) X and Y can be either (3,3), (5,5) or (9,5)
2) A player can be chosen from the following list:
"random": makes an arbitrary legal move
"minimax_brute": performs a brute-force minimax search
"minimax_depth": performs a minimax search over a desired number of levels in a search tree
"alpha_beta_brute": a minimax search with alpha-beta pruning, brute force
"alpha_beta_depth": a minimax search with alpha-beta pruning with a maximum depth level
3) depth_level_1 the depth level for 1st player (if applicable)
depth_level_2 the depth level for 2nd player (if applicable)
4) 

TODO 
DONE include an alpha beta player
DONE include number of states
DONE include an evaluation0
add BRUTE into alpha-beta and minimax 
include evaluation 2  
termination in a draw
"""
import random
import sys
import numpy as np


#
# def end_game(state):
#     _, nwhite, nblack = terminal(state)
#     if (nwhite==2 and nblack==2) or (nwhite==0 or nblack==0):
#         return (True, nwhite, nblack)
#     else:
#         return (False, nwhite, nblack)
#
# def check_end_game(state, nstates1, nstates2):
#     end, nwhite, nblack = end_game(state)
#     if end:
#         if nwhite == nblack:
#             result = "Draw"
#         if nwhite == 0:
#             result = "Player 2 won. Number of states visited:" + str(nstates2) + " Player 1 lose. Number of states visited:" + str(nstates1)
#         if nblack == 0:
#             result = "Player 1 won. Number of states visited:" + str(nstates1)+ " Player 2 lose. Number of states visited:" + str(nstates2)
#         print(result)
#         return True

def print_winner1(nstates1, nstates2):
    print("Player 1 won. Number of states visited:" + str(nstates1) + " Player 2 lose. Number of states visited:" + str(
        nstates2))


def print_winner2(nstates1, nstates2):
    print("Player 2 won. Number of states visited:" + str(nstates2) + " Player 1 lose. Number of states visited:" + str(
        nstates1))


def print_draw(nstates1, nstates2):
    print("A draw! Player 1 visited ") + str(nstates1) + " states. Player 2 visited:" + str(nstates2) + " states."


def print_winner(nwhite, nblack, nstates1, nstates2):
    if nwhite == 0:
        print("Player 2 won. Number of states visited:" + str(
            nstates2) + " Player 1 lose. Number of states visited:" + str(nstates1))
    if nblack == 0:
        print("Player 1 won. Number of states visited:" + str(
            nstates1) + " Player 2 lose. Number of states visited:" + str(nstates2))


def end_game(state, nstates1, nstates2, player1, player2, side):
    ans, nwhite, nblack = terminal(state)
    if ans:
        print_winner(nwhite, nblack, nstates1, nstates2)
    elif nblack == 2 and nwhite == 2:
        best1, _, nstates1 = player1(state=state, rem_depth = 7, side = side, nstate = nstates1)
        best2, _, nstates2 = player2
        if best1 == 1:
            print_winner1(nstates1, nstates2)
            return True
        elif best2 == 1:
            print_winner2(nstates1, nstates2)
            return True
        else:
            print_draw(nstates1, nstates2)
            return True
    return False


def fanorona():
    global X
    global Y
    ###########################################################################################
    title = "Game against a minimax with depth limit 3 (Player 1) and a random player(Player 2) on 5x5 board"
    X = 5
    Y = 5
    state = initial_state(X, Y)
    first_side = 1
    print(title)
    nstates1 = 0
    nstates2 = 0
    for i in range(5):
        gamend = False
        while not gamend:
            print("Start" + str(i))
            _, state, nstates1 = max_choose_move(state, first_side, 1, nstates1)
            gamend = end_game(state, nstates1, nstates2, max_choose_move(), random_player(), side)
            if not gamend:
                state = random_player(state, other_side(first_side))
                nstates2 += 1
                gamend = end_game(state, nstates1, nstates2, max_choose_move(state=state,side=1, rem_depth=7, nstates=nstates1))
    ###########################################################################################
    title = "Game against a minimax with depth limit 1 (Player 1) and a random player(Player 2) on 5x5 board"
    X = 5
    Y = 5
    #############################################################################################

#
# def fanorona():
#     global X
#     global Y
#     ###########################################################################################
#     title = "Game against a minimax with depth limit 3 (Player 1) and a random player(Player 2) on 5x5 board"
#     X = 5
#     Y = 5
#     state = initial_state(X, Y)
#     first_side = 1
#     print(title)
#     nstates1 = 0
#     nstates2 = 0
#     for _ in range(5):
#         gamend = False
#         while not gamend:
#             _, state, nstates1 = max_choose_move(state, first_side, 1, nstates1)
#             gamend = check_end_game(state, nstates1, nstates2)
#             if not gamend:
#                 state = random_player(state, other_side(first_side))
#                 nstates2 += 1
#                 gamend = check_end_game(state, nstates1, nstates2)
#     ###########################################################################################
#     title = "Game against a minimax with depth limit 1 (Player 1) and a random player(Player 2) on 5x5 board"
#     X = 5
#     Y = 5
#     #############################################################################################


def random_player(state, side):
    suc = successors(state, side)
    move = random.choice(suc)
    return move


def terminal(state):
    num_black = 0
    num_white = 0
    for x in range(X):
        for y in range(Y):
            if state[y, x] == 1:
                num_white += 1
            elif state[y, x] == -1:
                num_black += 1
    ans = num_white == 0 or num_black == 0
    return ans, num_white, num_black


def payoff(side, nwhite):
    """Returns a payoff for the player """
    if nwhite == 0:
        if side == 1:
            return -1
        else:
            return 1
    else:  # nblack == 0
        if side == 1:
            return 1
        else:
            return -1


def evaluate(side, nwhite, nblack, type=1):
    # if side == 1:
    #     return (nwhite - nblack)/npieces
    # if side == -1:
    #     return (nblack - nwhite)/npieces
    if type == 1:
        return (nwhite - nblack) / npieces * side
    elif type == 0:
        return 0


def max_choose_move(state, side, rem_depth, nstates):
    # todo include brute force
    end, nwhite, nblack = terminal(state)
    if end:
        return payoff(side, nwhite), state, nstates
    if rem_depth == 0:
        return evaluate(side, nwhite, nblack), state, nstates
    move = None
    best = -10000
    suc = successors(state, side)
    # print("Remaining depth: ", rem_depth)
    # print("Successors")
    # print(len(suc))
    for s in suc:
        nstates += 1
        sval, _, nstates = min_choose_move(s, other_side(side), rem_depth - 1, nstates)
        if sval > best:
            best = sval
            move = s
    return best, move, nstates


def min_choose_move(state, side, rem_depth, nstates):
    end, nwhite, nblack = terminal(state)
    if end:
        return payoff(side, nwhite) * -1, state, nstates
    if rem_depth == 0:
        return evaluate(side, nwhite, nblack) * -1, state, nstates
    move = None
    best = 10000
    suc = successors(state, side)
    # print("Remaining depth: ", rem_depth)
    # print("Successors")
    # print(len(suc))
    for s in suc:
        nstates += 1
        sval, _, nstates = max_choose_move(s, other_side(side), rem_depth - 1, nstates)
        if sval < best:
            best = sval
            move = s
    return best, move, nstates


def max_value(state, side, rem_depth, nstates, alpha=-1000, beta=1000):
    # at first iteration alpha is a large positive number, beta is a large negative numbers
    end, nwhite, nblack = terminal(state)
    if end:
        return payoff(side, nwhite), state, nstates
    if rem_depth == 0:
        return evaluate(side, nwhite, nblack), state, nstates
    move = None
    suc = successors(state, side)
    # print("Remaining depth: ", rem_depth)
    # print("Successors")
    # print(len(suc))
    for s in suc:
        nstates += 1
        sval, _, nstates = min_value(s, other_side(side), rem_depth - 1, nstates, alpha, beta)
        if sval > alpha:
            alpha = sval
            move = s
        if alpha > beta:
            return beta, move, nstates
    return alpha, move, nstates


def min_value(state, side, rem_depth, nstates, alpha, beta):
    end, nwhite, nblack = terminal(state)
    if end:
        return payoff(side, nwhite) * -1, state, nstates
    if rem_depth == 0:
        return evaluate(side, nwhite, nblack) * -1, state, nstates
    move = None
    suc = successors(state, side)
    # print("Remaining depth: ", rem_depth)
    # print("Successors")
    # print(len(suc))
    for s in suc:
        nstates += 1
        sval, _, nstates = max_value(s, other_side(side), rem_depth - 1, nstates, alpha, beta)
        if sval < beta:
            beta = sval
            move = s
        if beta < alpha:
            return alpha, s, nstates
    return beta, move, nstates


def initial_state(x, y):
    global npieces
    state = np.zeros((y, x), dtype=np.int8)
    if x == 3 and y == 3:
        state[2, :] = 1
        state[0, :] = -1
        state[1, 0] = 1
        state[1, 2] = -1
        npieces = 4
    elif x == 5 and y == 5:
        state[0:2, :] = -1
        state[2, 0] = -1
        state[2, 1] = 1
        state[2, 3] = -1
        state[2, 4] = 1
        state[3:5, :] = 1
        npieces = 7
    elif x == 9 and y == 5:
        state[0:2, :] = -1
        state[3:5, :] = 1
        state[2, [0, 2, 5, 7]] = -1
        state[2, [1, 3, 6, 8]] = 1
        npieces = 22
    else:
        raise ValueError("Unsupported dimensions. Must be (9,5), (5,5) or (3,3)")
    return state


def other_side(side):
    if side == 1:
        return -1
    elif side == -1:
        return 1
    else:
        raise ValueError("Invalid value of side, must be 1 or -1")


def move_up(state, crd, side, cands):  # be careful, modifies cands! non fruitfuls function
    x, y = crd
    # y and x are switched to access the elements of an numpy array (i.e. #rows, #elements)#
    if state[y, x] != side:  # wrong side
        return
    elif y - 1 < 0:  # out of the board
        return
    elif state[y - 1, x] != 0:  # an intersection is not empty
        return
    else:
        # capture by approach
        state_new = state.copy()
        state_new[y, x] = 0
        state_new[y - 1, x] = side
        y_opponent = y - 2
        while y_opponent >= 0 and state[y_opponent, x] == other_side(side):
            state_new[y_opponent, x] = 0
            y_opponent -= 1
        cands.append(state_new)

        # capture by retreat
        state_new = state.copy()
        state_new[y, x] = 0
        state_new[y - 1, x] = side
        y_opponent = y + 1
        while y_opponent < Y and state[y_opponent, x] == other_side(side):
            state_new[y_opponent, x] = 0
            y_opponent += 1
        cands.append(state_new)


def set_delta(direction):
    if direction == "up":
        delta_y = -1
        delta_x = 0
    elif direction == "down":
        delta_y = 1
        delta_x = 0
    elif direction == "right":
        delta_y = 0
        delta_x = 1
    elif direction == "left":
        delta_y = 0
        delta_x = -1
    elif direction == "upright":
        delta_y = -1
        delta_x = 1
    elif direction == "upleft":
        delta_y = -1
        delta_x = -1
    elif direction == "downright":
        delta_y = 1
        delta_x = 1
    elif direction == "downleft":
        delta_y = 1
        delta_x = -1
    else:
        raise ValueError("Unsupported direction!")
    return delta_x, delta_y


def move(state, crd, side, cands, direction):  # be careful, modifies cands! non fruitfuls function
    delta_x, delta_y = set_delta(direction)
    x, y = crd
    x_new = x + delta_x
    y_new = y + delta_y
    # y and x are switched to access the elements of an numpy array (i.e. #rows, #elements)#
    if state[y, x] != side:  # wrong side
        return
    elif not inboard(x_new, y_new):
        return
    elif state[y_new, x_new] != 0:  # next intersection is not empty
        return
    else:
        # capture by approach
        state_approach = state.copy()
        state_approach[y, x] = 0
        state_approach[y_new, x_new] = side
        y_opponent = y_new + delta_y * 1
        x_opponent = x_new + delta_x * 1
        c_approach = 0
        while inboard(x_opponent, y_opponent) and state[y_opponent, x_opponent] == other_side(side):
            state_approach[y_opponent, x_opponent] = 0
            y_opponent += delta_y
            x_opponent += delta_x
            c_approach += 1

        # capture by retreat
        state_retreat = state.copy()
        state_retreat[y, x] = 0
        state_retreat[y_new, x_new] = side
        y_opponent = y - delta_y * 1
        x_opponent = x - delta_x * 1
        c_retreat = 0
        while inboard(x_opponent, y_opponent) and state[y_opponent, x_opponent] == other_side(side):
            state_retreat[y_opponent, x_opponent] = 0
            c_retreat += 1
            y_opponent -= delta_y
            x_opponent -= delta_x
        if c_approach == 0 and c_retreat > 0:
            cands.append(state_retreat)
        elif c_approach > 0 and c_retreat == 0:
            cands.append(state_approach)
        elif c_approach > 0 and c_retreat > 0:
            cands.append(state_approach)
            cands.append(state_retreat)
        else:
            cands.append(state_approach)  # approach and retreat move are identical


def inboard(x_new, y_new):
    res = y_new >= 0 and y_new < Y and x_new >= 0 and x_new < X
    return res


def print_arrays(list):
    for i in list:
        print(i)


def successors(state, side):
    suc = []
    for x in range(X):
        for y in range(Y):
            if state[y, x] == side:
                cand = []
                move(state, (x, y), side, cand, "up")
                move(state, (x, y), side, cand, "down")
                move(state, (x, y), side, cand, "right")
                move(state, (x, y), side, cand, "left")
                if abs(x - y) % 2 == 0:
                    move(state, (x, y), side, cand, "upright")
                    move(state, (x, y), side, cand, "upleft")
                    move(state, (x, y), side, cand, "downright")
                    move(state, (x, y), side, cand, "downleft")
                if cand:
                    suc = suc + cand
    return suc


def testing_successors():
    global X, Y
    X = 5
    Y = 5
    instate = np.zeros((X, Y), dtype=np.int8)
    instate[1, 0] = 1
    instate[2, 0] = 1
    instate[4, 0] = -1
    instate[1, 1] = -1
    instate[4, 1] = 1
    instate[2, 2] = 1
    instate[0, 3] = 1
    instate[2, 3] = -1
    instate[3, 3] = 1
    instate[0, 4] = 1
    print("===============TESTING SUCCESSORS=============")
    print("INSTATE: \n", instate)
    suc = successors(instate, -1)
    print_arrays(suc)
    print(len(suc))
    terminal(instate)


def testing_max_choose():
    global X, Y
    X = 5
    Y = 5
    instate = np.zeros((X, Y), dtype=np.int8)
    instate[1, 0] = -1
    instate[1, 1] = -1
    instate[1, 2] = 1
    instate[1, 3] = -1
    instate[1, 4] = -1
    instate[4, 4] = -1
    global npieces
    npieces = 7
    print("Initial state \n")
    print(instate)
    depth = 6
    print("Min-max algorithm with maximum depth " + str(depth))
    print(max_choose_move(instate, -1, depth, 0))
    print("Alpha beta algorithm with maximum depth " + str(str(depth)))
    print(max_value(instate, -1, depth, 0, -1000, 1000))


def testing_move():
    global X, Y
    X = 3
    Y = 3
    instate = initial_state(X, Y)
    print(instate)
    successors = []
    print("Moving (1,2) up")
    move_up(instate, (1, 2), 1, successors)
    print(successors)
    print("====================CAPTURE BY RETREAT AND APPROACH====================")
    X = 5
    Y = 5
    instate = np.zeros((X, Y), dtype=np.int8)
    instate[0, 3] = 1
    instate[2, 3] = -1
    instate[3, 3] = 1
    instate[4, 3] = 1
    print(instate)
    successors = []
    print("moving up (3,2,-1)")
    move_up(instate, (3, 2), -1, successors)
    print_arrays(successors)
    print("moving up (3,2,1)")
    successors = []
    move_up(instate, (3, 2), 1, successors)
    print_arrays(successors)
    print("====================TESTING GENERAL MOVE FUNCTION====================")
    print("====================TESTING UP: A + R====================")
    print("moving up (3,2,-1)")
    successors = []
    move(instate, (3, 2), -1, successors, "up")
    print("====================TESTING DOWN: A ====================")
    instate = successors[0]
    print(instate)
    print("moving down (3,1,-1)")
    successors = []
    move(instate, (3, 1), -1, successors, "down")
    print_arrays(successors)
    print("====================TESTING DOWN: A + R====================")
    instate[0, 3] = 1
    print("Instate \n", instate)
    successors = []
    move(instate, (3, 1), -1, successors, "down")
    print_arrays(successors)
    print("====================TESTING RIGHT: Illegal====================")
    instate[2, 4] = -1
    print(instate)
    successors = []
    move(instate, (2, 4), -1, successors, "right")
    print_arrays(successors)
    print("====================TESTING DOWNLEFT: Legal + R====================")
    print("Instate: \n", instate)
    successors = []
    move(instate, (3, 3), 1, successors, "downleft")
    print_arrays(successors)
    print("====================TESTING UP: Legal + R====================")
    X = 5
    Y = 5
    instate = np.zeros((X, Y), dtype=np.int8)
    instate[1, 0] = 1
    instate[2, 0] = 1
    instate[4, 0] = -1
    instate[1, 1] = -1
    instate[4, 1] = 1
    instate[2, 2] = 1
    instate[0, 3] = 1
    instate[2, 3] = -1
    instate[3, 3] = 1
    instate[0, 4] = 1
    print("Instate:\n", instate)
    successors = []
    move(instate, (1, 1), -1, successors, "up")
    print_arrays(successors)


if __name__ == "__main__":
    # testing_move()
    # testing_successors()
    #testing_max_choose()
    # instate = initial_state(9,5)
     fanorona()
