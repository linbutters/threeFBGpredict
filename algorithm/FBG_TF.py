import tensorflow as tf
FOUR_LOG_TWO = 4.*tf.math.log(2.)

@tf.function
def simulate_TF(x_coord, X):
    """
    X = (NP, c/w/h, nFBG)
    """
    x_coord = tf.cast(tf.tile(x_coord[tf.newaxis, tf.newaxis, :],
                      [X.shape[0], X.shape[2], 1]), tf.dtypes.float32)
    c = X[:, 0][:, :, tf.newaxis]
    w = X[:, 1][:, :, tf.newaxis]
    h = X[:, 2][:, :, tf.newaxis]
    y = tf.exp(-((x_coord-c)/w)**2*FOUR_LOG_TWO)*h
    return tf.reduce_sum(y, 1)


# import matplotlib.pyplot as plt

# f = simulate(tf.linspace(0., 1., 10000), tf.constant([
#     [
#         [0.3, 0.7],
#         [0.1, 0.1],
#         [1, 0.5]
#     ]
# ], dtype=tf.dtypes.float32))

# plt.plot(tf.transpose(f))
# plt.show()
# print(f)
