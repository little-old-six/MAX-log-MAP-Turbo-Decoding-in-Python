from Tools import Cut, G_prob_0_1, H_compare
import numpy as np
from Transform import Trans, Re_Trans
from BCJR_dec import BCJR0
from Turbo_encode import *
import math


def Get_Pe(Pp0, Pa0):
    Pp1, Pa1 = 1 - Pp0, 1 - Pa0
    Pe1, Pe0 = Pp1 - Pa1, Pp0 - Pa0
    Pe1, Pe0 = math.e**Pe1, math.e**Pe0
    k = 1/(Pe1 + Pe0)
    Pe1, Pe0 = k*Pe1, k*Pe0
    return Pe0, Pe1


def Turbo(m, sigma, size, inter):
    a = Turbo_encode(size, m, sigma)
    m1_num, M0, U = a.Start()

    M1, M2 = Cut(M0)
    C2 = np.zeros(len(M1))
    P1_0, P1_1 = G_prob_0_1(M1, C2, m1_num, sigma)
    P2_0, P2_1 = G_prob_0_1(M2, C2, m1_num, sigma)

    Pa1_0 = np.ones(m1_num) * 0.5
    U_mes = []

    for H_int in range(inter):
        bcjr1 = BCJR0(m, m1_num, P1_0, P1_1, Pa1_0)
        Pp1_0, Pp1_1 = bcjr1.start()
        Pe1_0, Pe1_1 = Get_Pe(Pp1_0, Pa1_0)

        Pa2_0 = Trans(Pe1_0)
        bcjr2 = BCJR0(m, m1_num, P2_0, P2_1, Pa2_0)
        Pp2_0, Pp2_1 = bcjr2.start()
        Pe2_0, Pe2_1 = Get_Pe(Pp2_0, Pa2_0)

        Pa1_0 = Re_Trans(Pe2_0)

    Pp2_0, Pp2_1 = Re_Trans(Pp2_0), Re_Trans(Pp2_1)

    Lu = np.zeros(len(Pp2_1))
    for i in range(len(Pp2_1)):
        Lu[i] = Pp2_0[i] - Pp2_1[i]
        if Lu[i] <= 0:
            U_mes = U_mes + [1]
        else:
            U_mes = U_mes + [0]
    print('Lu:', np.round(np.array(Lu), 3))

    m = 0
    Pe = H_compare(U, U_mes, m) / (len(U)-m)
    R = 1 / 3
    SNR = 1 / (2 * (sigma ** 2) * R)

    return U_mes, SNR, Pe
