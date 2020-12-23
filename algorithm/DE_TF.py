import numpy as tf
import tensorflow as tf
import numpy as np


class DE_TF:
    def __init__(self, F=0.5, CR=0.5, NP=50):
        self.F = F
        self.CR = CR
        self.NP = NP
    
    def init(self, down_lim, up_lim):
        X = tf.random.uniform([self.NP, *up_lim.shape])
        X *= up_lim-down_lim
        X += down_lim
        return X

    def random_choose_abc(self):
        i = tf.range(self.NP)
        a = tf.random.uniform([self.NP],
                              maxval=self.NP - 1, dtype=tf.dtypes.int32)
        b = tf.random.uniform([self.NP],
                              maxval=self.NP - 2, dtype=tf.dtypes.int32)
        c = tf.random.uniform([self.NP],
                              maxval=self.NP - 3, dtype=tf.dtypes.int32)

        a += tf.cast(a >= i, tf.dtypes.int32)

        ia = tf.sort([i, a], 0)

        for last in ia:
            b += tf.cast(b >= last, tf.dtypes.int32)

        iab = tf.sort([i, a, b], 0)

        for last in iab:
            c += tf.cast(c >= last, tf.dtypes.int32)

        return a, b, c

    def random_choose_axis(self, X):
        random = tf.random.uniform(X.shape)
        random2 = tf.random.uniform(X.shape)
        maximum = tf.reduce_max(random, axis=1, keepdims=True)
        return tf.cast(tf.logical_or(random == maximum, random2 < self.CR), tf.dtypes.float32)

    def mutate(self, X):
        a, b, c = self.random_choose_abc()
        A = tf.gather(X, a)
        B = tf.gather(X, b)
        C = tf.gather(X, c)
        axis = self.random_choose_axis(X)
        Y = X + (A + self.F*(B-C)-X)*axis
        return Y

