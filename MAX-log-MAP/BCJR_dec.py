import numpy as np
import math
from Tools import O_state, G_next_state, G_out, G_in


class BCJR0():
    def __init__(self, m, m1_num, P0, P1, U0_p):
        self.m, self.m1_num, self.P0, self.P1, self.U0_p = m, m1_num, P0, P1, U0_p

    def start(self):
        self.C_trellis()
        self.G_tran_prob()
        self.G_A_prob()
        self.G_B_prob()
        self.BCJR_Decoding()
        return self.Pp_0, self.Pp_1

    def G_tran_prob(self):
        self.T = np.zeros(((2 ** self.m), (self.m1_num + 1), (2 ** self.m), (self.m1_num + 1)))
        J = 0
        while (J < self.m1_num):
            for i in range(2 ** self.m):
                for j in range(2 ** self.m):
                    if self.a[i, J, j, J + 1] != 0:
                        I1, J1, I2, J2 = O_state(i, j)
                        X_0, U_0 = G_out(I1, J1, I2, J2)
                        if U_0 == 0:
                            PU = self.U0_p[J]
                        else:
                            PU = 1 - self.U0_p[J]
                        if U_0 == 0:
                            PC1 = self.P0[2 * J]
                        else:
                            PC1 = self.P1[2 * J]
                        if X_0 == 0:
                            PC2 = self.P0[2 * J + 1]
                        else:
                            PC2 = self.P1[2 * J + 1]

                        self.T[i, J, j, J + 1] = math.log((PU * PC1 * PC2), math.e)
            J += 1

        for i in range(2 ** self.m):
            X1, X2 = G_next_state(i)
            for J in range(self.m1_num):
                self.T[i, J, X1, J + 1] = math.e ** self.T[i, J, X1, J + 1]
                self.T[i, J, X2, J + 1] = math.e ** self.T[i, J, X2, J + 1]
                k = 1 / (self.T[i, J, X1, J + 1] + self.T[i, J, X2, J + 1])
                self.T[i, J, X1, J + 1], self.T[i, J, X2, J + 1] = k * self.T[i, J, X1, J + 1], k * self.T[i, J, X2, J + 1]

    def G_A_prob(self):
        self.A = np.zeros((2 ** self.m, (self.m1_num + 1)))
        J = 1
        self.A[0, 0] = self.A[1, 0] = self.A[2, 0] = self.A[3, 0] = 1/4
        while J <= self.m1_num:
            for i in range(2 ** self.m):
                for j in range(2 ** self.m):
                    if self.a[j, J - 1, i, J] != 0:
                        self.A[i, J] = self.Max(self.A[i, J], (self.T[j, J - 1, i, J] + self.A[j, J - 1]))
            for ii in range(4):
                self.A[ii, J] = math.e ** self.A[ii, J]
            k = 1 / (self.A[0, J] + self.A[1, J] + self.A[2, J] + self.A[3, J])
            for i in range(2 ** self.m):
                self.A[i, J] = k * self.A[i, J]
            J += 1

    def G_B_prob(self):
        self.B = np.zeros((2 ** self.m, (self.m1_num + 1)))
        J = (self.m1_num - 1)
        self.B[3, self.m1_num] = self.B[1, self.m1_num] = self.B[2, self.m1_num] = self.B[0, self.m1_num] = 1/4
        while J > 0:
            for i in range(2 ** self.m):
                for j in range(2 ** self.m):
                    if self.a[i, J, j, J + 1] != 0:
                        self.B[i, J] = self.Max(self.B[i, J], (self.T[i, J, j, J + 1] + self.B[j, J + 1]))
            for ii in range(4):
                self.B[ii, J] = math.e ** self.B[ii, J]
            k = 1 / (self.B[0, J] + self.B[1, J] + self.B[2, J] + self.B[3, J])
            for i in range(2 ** self.m):
                self.B[i, J] = k * self.B[i, J]
            J -= 1

    def BCJR_Decoding(self):
        self.Pp_1 = np.ones(self.m1_num) * 10000
        self.Pp_0 = np.ones(self.m1_num) * 10000
        J = 0
        while J < self.m1_num:
            P1 = P0 = 0
            for i in range(2 ** self.m):
                for j in range(2 ** self.m):
                    if self.a[i, J, j, J + 1] == -1:
                        if P0 == 0:
                            P0 = self.T[i, J, j, J + 1] + self.A[i, J] + self.B[j, J + 1]
                        else:
                            P0 = self.Max(P0, (self.T[i, J, j, J + 1] + self.A[i, J] + self.B[j, J + 1]))
                    elif self.a[i, J, j, J + 1] == 1:
                        if P1 == 0:
                            P1 = self.T[i, J, j, J + 1] + self.A[i, J] + self.B[j, J + 1]
                        else:
                            P1 = self.Max(P1, (self.T[i, J, j, J + 1] + self.A[i, J] + self.B[j, J + 1]))
            P1, P0 = math.e**P1, math.e**P0
            k = 1 / (P1 + P0)
            P0, P1 = k * P0, k * P1
            self.Pp_0[J], self.Pp_1[J] = P0, P1
            J += 1
        return self.Pp_0, self.Pp_1

    def C_trellis(self):
        self.a = np.zeros(((2 ** self.m), (self.m1_num + 1), (2 ** self.m), (self.m1_num + 1)))
        for j in range(self.m1_num):
            for i in range(2 ** self.m):
                X = G_in(0, i)
                self.a[i, j, X, (j + 1)] = -1

                X = G_in(1, i)
                self.a[i, j, X, (j + 1)] = 1

    def Max(self, x, y):
        # z0 = 1 + math.e**(-(abs(x-y))) # choose this when log-MAP
        z0 = 1                           # choose this when Max-log -MAP
        z = max(x, y) + math.log(z0, math.e)
        return z

