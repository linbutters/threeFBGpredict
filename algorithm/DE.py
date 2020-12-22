import numpy as np


class DE:
    def __init__(self, F, CR, NP):
        self.F = F
        self.CR = CR
        self.NP = NP

    def init(self, down_lim, up_lim):
        X = np.random.rand(self.NP, *up_lim.shape)
        X *= up_lim-down_lim
        X += down_lim
        return X

    def random_choose_abc(self):
        i = np.arange(self.NP)
        a = np.random.randint(self.NP-1, size=(self.NP))
        b = np.random.randint(self.NP-2, size=(self.NP))
        c = np.random.randint(self.NP-3, size=(self.NP))

        a += a >= i

        ia = np.sort(np.array([i, a]), 0)

        for last in ia:
            b += b >= last

        iab = np.sort(np.array([i, a, b]), 0)

        for last in iab:
            c += c >= last

        return a, b, c

    def random_choose_axis(self, X):
        random = np.random.rand(*X.shape)
        random2 = np.random.rand(*X.shape)
        maximum = np.max(random, axis=1, keepdims=True)
        return np.logical_or(random == maximum, random2 < self.CR)

    def mutate(self, X):
        a, b, c = self.random_choose_abc()
        A = X[a]
        B = X[b]
        C = X[c]
        axis = self.random_choose_axis(X)
        U = np.random.rand(*X.shape)
        Y = X + (A + self.F*(B-C)-X)*axis
        return Y