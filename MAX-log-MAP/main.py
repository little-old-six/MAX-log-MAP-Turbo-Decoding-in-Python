from Turbo_main import Turbo

if __name__ == '__main__':

    m = 2             # number of registers in this conv. code
    sigma = 1         # Standard deviation of AWGN in channel
    size = 5          # number of message bits
    inter = 10         # Number of iterations

    U_mes, SNR, Pe = Turbo(m, sigma, size, inter)
    print('Turbo decoding result:', U_mes)
    print('SNR=', SNR, '     ', 'Pe', Pe)
    print('over')

















    # X = Y =[]
    # for i in sigma:
    #     U_mes, SNR, Pe = Turbo(m, i, size, inter)
    #     X = X + [SNR]
    #     Y = Y + [Pe]
    #
    # X = np.array(X)
    # Y = np.array(Y)
    # Fig_plot(X, Y)




