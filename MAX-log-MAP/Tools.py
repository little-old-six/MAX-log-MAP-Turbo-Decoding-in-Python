import numpy as np
import math
from Transform import Trans

def G_out(i1, j1, i2, j2):
    x = i1 * 10 + j1
    y = i2 * 10 + j2
    if (x == 0) and (y == 0):
        return 0, 0
    elif x == 0 and y == 10:
        return 1, 1
    elif x == 1 and y == 0:
        return 0, 1
    elif x == 1 and y == 10:
        return 1, 0
    elif x == 10 and y == 1:
        return 0, 0
    elif x == 10 and y == 11:
        return 1, 1
    elif x == 11 and y == 1:
        return 0, 1
    elif x == 11 and y == 11:
        return 1, 0


def O_state(I, J):
    X1 = Y1 = X2 = Y2 = 0
    if I == 0:
        X1 = Y1 = 0
    elif I == 1:
        X1, Y1 = 0, 1
    elif I == 2:
        X1, Y1 = 1, 0
    elif I == 3:
        X1 = Y1 = 1
    if J == 0:
        X2 = Y2 = 0
    elif J == 1:
        X2, Y2 = 0, 1
    elif J == 2:
        X2, Y2 = 1, 0
    elif J == 3:
        X2 = Y2 = 1
    return X1, Y1, X2, Y2


def G_in(x, I):
    Y = 5
    if (I == 0) and (x == 0):
        Y = 0
    elif (I == 0) and (x == 1):
        Y = 2
    if (I == 1) and (x == 0):
        Y = 2
    elif (I == 1) and (x == 1):
        Y = 0
    if (I == 2) and (x == 0):
        Y = 1
    elif (I == 2) and (x == 1):
        Y = 3
    if (I == 3) and (x == 0):
        Y = 3
    elif (I == 3) and (x == 1):
        Y = 1
    return Y


def G_prob(X, Y, sigma):
    N0 = 2*(sigma**2)
    x1, y1 = 1, 0
    x2, y2 = -1, 0
    P0 = 1 / np.sqrt((np.pi * N0)) * math.exp((-(((X - x1)**2 + (Y - y1)**2)/N0)))
    P1 = 1 / np.sqrt((np.pi * N0)) * math.exp((-(((X - x2) ** 2 + (Y - y2) ** 2) / N0)))
    k = 1 / (P0+P1)
    P0 = P0 * k
    P1 = P1 * k
    return P0, P1


def Cut(M0):
    l = len(M0)
    C0 = C1 = C2 = M1 = M2 = []
    h = 0
    for i in range(l):
        if h == 0:
            C0 = C0 + [M0[i]]
            h = 1
        elif h == 1:
            C1 = C1 + [M0[i]]
            h = 2
        elif h == 2:
            C2 = C2 + [M0[i]]
            h = 0
    C0_2 = Trans(C0)
    for i in range(len(C1)):
        M1 = M1 + [C0[i]] + [C1[i]]
        M2 = M2 + [C0_2[i]] + [C2[i]]
    return M1, M2


def G_prob_0_1(C1, C2, m1_num, sigma):
    P1 = P0 = []
    for i in range(2*m1_num):
        p0, p1 = G_prob(C1[i], C2[i], sigma)
        P1 = P1 + [p1]
        P0 = P0 + [p0]
    return P0, P1


def G_next_state(I):
    if (I == 0) or (I == 1):
        return 0, 2
    elif (I == 2) or (I == 3):
        return 1, 3


def H_compare(M0, M1, m):
    dis = 0
    l = len(M0)
    for i in range(l- m ):
        if M1[i] != M0[i]:
            dis += 1
    return dis