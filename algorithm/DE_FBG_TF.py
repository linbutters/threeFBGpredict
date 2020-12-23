from algorithm.DE_TF import DE_TF
import tensorflow as tf
from algorithm.FBG_TF import simulate_TF

def iterate(de):
    @tf.function
    def f(data, X, PX, Perror):
        if Perror[0] >= 0:
            X = de.mutate(PX)
        spectra = simulate_TF(data[0], X)
        error = tf.reduce_sum((spectra - tf.cast(data[1, tf.newaxis, :], tf.dtypes.float32))**2, 1)

        if Perror[0] >= 0:
            compare = tf.cast(error < Perror, tf.dtypes.float32)
            PX += (X-PX) * compare[:, tf.newaxis, tf.newaxis]
            Perror += (error-Perror) * compare
        else:
            Perror = error
            PX = X
        return data, X, PX, Perror

    return f


def optimize_TF(data, center, width, height, d, iterations=20, F=.5, CR=0.1, NP=50):
    x = tf.constant([center, width, height], dtype=tf.dtypes.float32)

    down_lim = x - d[:, tf.newaxis]
    up_lim = x + d[:, tf.newaxis]

    de = DE_TF(F, CR, NP)

    X = de.init(down_lim, up_lim)

    Perror = tf.ones(X.shape[0]) * -1
    PX = X

    data, X, PX, Perror = tf.while_loop(lambda a, b, c, d: True,
                                        iterate(de), (data, X, PX, Perror),
                                        maximum_iterations=iterations)

    average = tf.math.reduce_mean(PX, 0)
    return average
