import numpy as np
from Transform import Trans


class Turbo_encode:
    def __init__(self, size, m, sigma):
        self.size = size
        self.m = m
        self.sigma = sigma

    def Start(self):
        return self.Encode()

    def C_relationship(self, S, I):
        if (S == 0) and (I == 0):
            return 0, 0
        elif (S == 0) and (I == 1):
            return 10, 1
        elif (S == 1) and (I == 0):
            return 10, 1
        elif (S == 1) and (I == 1):
            return 0, 0
        elif (S == 10) and (I == 0):
            return 1, 0
        elif (S == 10) and (I == 1):
            return 11, 1
        elif (S == 11) and (I == 0):
            return 11, 1
        elif (S == 11) and (I == 1):
            return 1, 0

    def BPSK_AWGN(self, M):
        M0 = []
        for i in M:
            if i == 0:
                M0 = M0 + [1]
            elif i == 1:
                M0 = M0 + [-1]
        mu = 0
        N = self.sigma * np.random.normal(mu, 1, len(M0))
        for i in range(len(M0)):
            M0[i] = M0[i] + N[i]
        return M0

    def Encode(self):
        U = np.random.randint(0, 2, (self.size))
        U = list(U)
        M1 = M2 = []
        m_num = len(U)
        print('Origional message symbol：', U)
        U0 = U.copy()
        B0 = self.BPSK_AWGN(U0)
        S = 0
        for i in range(m_num):
            S, X0 = self.C_relationship(S, U[i])
            M1 = M1 + [X0]
        B1 = self.BPSK_AWGN(M1)
        U2 = Trans(U)
        S = 0
        for i in range(m_num):
            S, X0 = self.C_relationship(S, U2[i])
            M2 = M2 + [X0]
        B2 = self.BPSK_AWGN(M2)
        B = self.add_sum(B0, B1, B2)
        self.Get_pattern(m_num)
        BB = np.round(np.array(B), 2)
        print('Codeword symbols:', BB)
        return m_num, B, U0

    def add_sum(self, B0, B1, B2):
        B = []
        l = len(B1)
        for i in range(l):
            B = B + [B0[i]] + [B1[i]] + [B2[i]]
        return B

    def Punch(self, B0, B1, B2):
        B1_new = B2_new = []
        l = len(B1)
        B0_2 = Trans(B0)
        for i in range(l):
            B1_new = B1_new + [B0[i]] + [B1[i]]
            B2_new = B2_new + [B0_2[i]] + [B2[i]]
        return B1_new, B2_new

    def Get_pattern(self, m_num):
        P = np.zeros(m_num)
        for i in range(m_num):
            P[i] = i + 1
        print('The interleaving pattern is:', Trans(P))