import numpy as np
import random

seed = 1


def Trans(a):
    a = a.copy()
    N = np.arange(1, (len(a)+1), 1)
    N = list(N)
    random.seed(seed)
    random.shuffle(N)
    a1 = np.zeros(len(a))
    for i in range(len(a)):
        a1[i] = a[(N[i]-1)]
    return a1


def Re_Trans(a):
    a = a.copy()
    N = np.arange(1, (len(a) + 1), 1)
    N = list(N)
    random.seed(seed)
    random.shuffle(N)
    a1 = np.zeros(len(a))
    for i in range(len(a)):
         a1[(N[i]-1)] = a[i]
    return a1