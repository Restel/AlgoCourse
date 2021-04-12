__author__ = 'Lina Brilliantova, RIT'
"""A program that plays the game fanorona. Implements a random player, a brute minimax solver, and a minimax with alpha beta prunning. Supports a maximum depth limit.   
Usage: python3 fanorona.py [id of experiment]
e.g. python3 fanorona.py 1
"""
import random
import sys
import numpy as np


def print_winner1(nstates1, nstates2):
    print("Player 1 won. Number of states visited:" + str(nstates1) + " Player 2 lose. Number of states visited:" + str(
        nstates2))


def print_winner2(nstates1, nstates2):
    print("Player 2 won. Number of states visited:" + str(nstates2) + " Player 1 lose. Number of states visited:" + str(
        nstates1))


def print_draw(nstates1, nstates2):
    print("A draw! Player 1 visited " + str(nstates1) + " states. Player 2 visited:" + str(nstates2) + " states.")


def print_winner(nwhite, nblack, nstates1, nstates2):
    if nwhite == 0:
        print("Player 2 won. Number of states visited:" + str(
            nstates2) + " Player 1 lose. Number of states visited:" + str(nstates1))
    if nblack == 0:
        print("Player 1 won. Number of states visited:" + str(
            nstates1) + " Player 2 lose. Number of states visited:" + str(nstates2))


def end_game(state, nstates1, nstates2, player1, player2, evaltype1, evaltype2, alpha, beta):
    ans, nwhite, nblack = terminal(state)
    if ans:
        print_winner(nwhite, nblack, nstates1, nstates2)
        return True
    elif nblack <= 2 and nwhite <= 2:
        best1, _, _ = player1(state=state, rem_depth = 7, side = 1, nstates = nstates1, evaltype = evaltype1, alpha = alpha, beta = beta)
        best2, _, _ = player2(state=state, rem_depth = 7, side = -1, nstates = nstates2, evaltype = evaltype2, alpha = alpha, beta = beta)
        if best1 == 1 or best2 == 1:
            return False # can not declare a draw yet
        else: # no one sees the win in 7 steps and both sides have few pieces -> a draw
            print_draw(nstates1, nstates2)
            return True
    return False

def play_against(crd, title, player1, player2, evaltype1, evaltype2, rem_depth1, rem_depth2, alpha = -1000, beta = 1000):
    """

    :param crd: a tuple with dimensions of the board
    :param title: title of the trial
    :param player1: algorithm to play for white
    :param player2:algorithm to play for black
    :param evaltype1: the type of evaluation function for Player 1
    :param evaltype2:the type of evaluation function for Player 2
    :param rem_depth1: the maximum depth for Player 1
    :param rem_depth2: the maximum depth for Player 1
    :return: None
    """
    print(title)
    global X,Y
    X,Y = crd
    state = initial_state(X, Y)
    nstates1 = 0
    nstates2 = 0
    gamend = False
    first_side = 1
    i = 0
    while not gamend:
        i += 1

        best, state, nstates1 = player1(state, first_side, rem_depth1, nstates1, evaltype=evaltype1, alpha = alpha, beta = beta)
        # print(rem_depth1)
        # print("Iteration", i)
        # print("State \n", state)
        # print("Best value", best)
        # print("Number os states", nstates1)

        gamend = end_game(state, nstates1, nstates2, player1, player2,
                          evaltype1=evaltype1, evaltype2=evaltype2, alpha = alpha, beta = beta)
        if not gamend:
            i += 1

            best, state, nstates2 = player2(state, other_side(first_side), rem_depth2, nstates2, evaltype=evaltype2, alpha = alpha, beta = beta)
            # print("Iteration", i)
            # print("State \n", state)
            # print("Best value", best)
            # print("Number of states", nstates2)
            gamend = end_game(state, nstates1, nstates2, player1, player2,
                              evaltype1=evaltype1, evaltype2=evaltype2, alpha = alpha, beta = beta)

def play_game(exp):
    if exp == '1':
        for i in range(2,5):
            title = "Player1: Brute-force with depth limit {0} and zero evaluation function, Player2: same on 3X3 board".format(i)
            play_against(crd = (3, 3), title = title,
                         player1 = max_choose_move, player2 =  max_choose_move, evaltype1 =  0, evaltype2 = 0, rem_depth1=i, rem_depth2=i)
    if exp == '2':
        for i in range(5):
          play_against((5,5), "Player 1: random player, Player 2: Brute with depth limit 2 on 5x5 board. Evaluation function 1", random_player, max_choose_move, 1, 1, rem_depth1 = 1, rem_depth2 = 2)

    if exp == '3':
        for eval in range(1,3):
            for depth in range(3,4):
                title = "Brute-force with limit 1 vs brute-force with limit {0}, Evaluation function {1} function on 5x5 board".format(depth,eval)
                play_against((5, 5),
                             title,
                             max_choose_move, max_choose_move, eval, eval, rem_depth1=1, rem_depth2=depth)

    if exp == '4':
        for depth in range(3,5):
            title = "Player1: Alpha-beta with limit {0} and Evaluation function 1, Player 2: Alpha-beta with limit {0} and Evaluation function 2 on 5x5".format(depth)
            if depth == 4: title = title + "\n Attention: takes a lot of time (up to 10 mins) to produce result"
            play_against((5, 5), title,
                         max_value, max_value, evaltype1=1, evaltype2=2, rem_depth1=depth, rem_depth2=depth, alpha=-1000,
                         beta=1000)

    if exp == '5':
        depth = 2
        title = "Player1: Brute solver with limit {0} and Evaluation function 1, Player 2: Brute solver with limit {0} and Evaluation function 2 on 5x5".format(depth)
        play_against((5, 5),
                     title,
                     max_choose_move, max_choose_move, 1, 2, rem_depth1=depth, rem_depth2=depth)
        depth = 3
        title = "Player1: Brute solver with limit {0} and Evaluation function 1, Player 2: Brute solver with limit {0} and Evaluation function 2 on 5x5".format(
            depth)
        title += "\n Attention: takes a lot of time (up to 30 mins) to produce result"
        play_against((5, 5),
                     title,
                     max_choose_move, max_choose_move, 1, 2, rem_depth1=depth, rem_depth2=depth)
        depth = 4
        title = "Player1: Brute solver with limit {0} and Evaluation finction 1, Player 2: Brute solver with limit {0} and Evaluation function 2 on 5x5".format(
            depth)
        title += "\n Attention: takes a lot of time (up to 30 mins) to produce result"
        play_against((5, 5),
                     title,
                     max_choose_move, max_choose_move, 1, 2, rem_depth1=depth, rem_depth2=depth)


def random_player(state, side, rem_depth, nstates, evaltype, alpha = 1000, beta = -1000):
    suc = successors(state, side)
    move = random.choice(suc)
    return None, move, nstates+1


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

def on_board_edge(x,y):
    if x == 0 or y == 0 or x == X-1 or y == Y-1:
        return True
    else: return False

def evaluate_connections(state, side):
    sum = 0
    for x in range(X):
        for y in range(Y):
            if state[y,x] == side:
                sum += ncount[y,x]
    return sum

def count_side_pieces(side, nwhite, nblack):
    if side == 1:
        return nwhite
    elif side == -1:
        return nblack
    else:
        raise ValueError

def evaluate(state, side, nwhite, nblack, type):
    """

    :param side: the side (1,-1) for which the evaluation is performed
    :param nwhite: number of white pieces
    :param nblack: number of black pieces
    :param type: the type of the evaluation function
    :return: predicted payoff - real number in range [-1, 1]
    """
    # if side == 1:
    #     return (nwhite - nblack)/npieces
    # if side == -1:
    #     return (nblack - nwhite)/npieces
    ans = None
    if type == 1:
        ans = (nwhite - nblack) / npieces * side
    elif type == 0:
        ans = 0
    elif type == 2:
        E_s = evaluate_connections(state, side)
        E_os = evaluate_connections(state, other_side(side))
        P_s = count_side_pieces(side, nwhite, nblack)
        P_os = count_side_pieces(other_side(side), nwhite, nblack)
        denom = npieces * nedges
        ans = (E_s * P_s - E_os * P_os)/denom
    else: raise ValueError("Unsupported evaluation type")
    return ans

def max_choose_move(state, side, rem_depth, nstates, evaltype, alpha = 0, beta = 0):
    end, nwhite, nblack = terminal(state)
    if end:
        return payoff(side, nwhite), state, nstates
    if rem_depth == 0:
        return evaluate(state, side, nwhite, nblack, evaltype), state, nstates
    move = None
    best = -10000
    suc = successors(state, side)
    # print("Remaining depth: ", rem_depth)
    # print("Successors")
    # print(len(suc))
    for s in suc:
        nstates += 1
        sval, _, nstates = min_choose_move(s, other_side(side), rem_depth - 1, nstates, evaltype)
        if sval > best:
            best = sval
            move = s
    return best, move, nstates


def min_choose_move(state, side, rem_depth, nstates, evaltype, alpha = 0, beta = 0):
    end, nwhite, nblack = terminal(state)
    if end:
        return payoff(side, nwhite) * -1, state, nstates
    if rem_depth == 0:
        return evaluate(state,side, nwhite, nblack, evaltype) * -1, state, nstates
    move = None
    best = 10000
    suc = successors(state, side)
    # print("Remaining depth: ", rem_depth)
    # print("Successors")
    # print(len(suc))
    for s in suc:
        nstates += 1
        sval, _, nstates = max_choose_move(s, other_side(side), rem_depth - 1, nstates, evaltype)
        if sval < best:
            best = sval
            move = s
    return best, move, nstates


def max_value(state, side, rem_depth, nstates, alpha, beta, evaltype=1):
    # at first iteration alpha is a large positive number, beta is a large negative numbers
    end, nwhite, nblack = terminal(state)
    if end:
        return payoff(side, nwhite), state, nstates
    if rem_depth == 0:
        return evaluate(state, side, nwhite, nblack, type = evaltype), state, nstates
    move = None
    suc = successors(state, side)
    # print("Remaining depth: ", rem_depth)
    # print("Successors")
    # print(len(suc))
    for s in suc:
        nstates += 1
        sval, _, nstates = min_value(s, other_side(side), rem_depth - 1, nstates, alpha, beta, evaltype)
        if sval > alpha:
            alpha = sval
            move = s
        if alpha > beta:
            return beta, move, nstates
    # if move is None:
    #     print("debug")
    return alpha, move, nstates


def min_value(state, side, rem_depth, nstates, alpha, beta, evaltype):
    end, nwhite, nblack = terminal(state)
    if end:
        return payoff(side, nwhite) * -1, state, nstates
    if rem_depth == 0:
        return evaluate(state,side, nwhite, nblack, type = evaltype) * -1, state, nstates
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

def count_degree(x,y):
    count = np.zeros((y,x), dtype=np.int8)
    for i in range(x):
        if i == 0 or i == x - 1:
            count[:,i] = 3
            continue
        for j in range(y):
            if j == 0 or j == y - 1:
                count[j, :] = 3
                continue
            elif abs(i-j)%2==0:
                count[j,i] = 8
            else: count[j,i] = 4
    return count

def initial_state(x, y):
    global npieces # initial number of pieces per side
    global nedges # total number of connections between intersections
    global ncount
    state = np.zeros((y, x), dtype=np.int8)
    ncount = count_degree(x,y)
    if x == 3 and y == 3:
        state[2, :] = 1
        state[0, :] = -1
        state[1, 0] = 1
        state[1, 2] = -1
        npieces = 4
        nedges = (32 - 8)/2
    elif x == 5 and y == 5:
        state[0:2, :] = -1
        state[2, 0] = -1
        state[2, 1] = 1
        state[2, 3] = -1
        state[2, 4] = 1
        state[3:5, :] = 1
        npieces = 12
        nedges = (104-8)/2
    elif x == 9 and y == 5:
        state[0:2, :] = -1
        state[3:5, :] = 1
        state[2, [0, 2, 5, 7]] = -1
        state[2, [1, 3, 6, 8]] = 1
        npieces = 22
        nedges = (200-8)/2
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


def move(state, crd, side, cands, direction):
    delta_x, delta_y = set_delta(direction)
    x, y = crd
    x_new = x + delta_x
    y_new = y + delta_y
    # y and x are switched to access the elements of an numpy array in the form [#rows, #elements]
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
        y_opponent = y_new + delta_y
        x_opponent = x_new + delta_x
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
        y_opponent = y - delta_y
        x_opponent = x - delta_x
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
    depth = 4
    print("Min-max algorithm with maximum depth " + str(depth))
    print(max_choose_move(instate, -1, depth, 0, 1))
    print("Alpha beta algorithm with maximum depth " + str(str(depth)))
    print(max_value(instate, -1, depth, 0, -1000, 1000, 1))

def testing_eval():
    global X,Y
    X = 5
    Y = 5
    instate = initial_state(5,5)
    _, nwhite, nblack = terminal(instate)
    print(evaluate(instate, 1, nwhite, nblack, 3))
    instate[3,3] = 0
    _, nwhite, nblack = terminal(instate)
    print(evaluate(instate, 1, nwhite, nblack, 3))
def testing_move():
    global X, Y
    X = 3
    Y = 3
    instate = initial_state(X, Y)
    print(instate)
    successors = []
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
    # testing_max_choose()
    # instate = initial_state(9,5)
    #testing_eval()
    id = sys.argv[1]
    play_game(id)