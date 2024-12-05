import tensorflow as tf


def call_t(x1, x2, dim_less=False):
    dist1 = tf.math.square(x1 - x2)
    dist1 = tf.reduce_sum(tf.reshape(dist1, [tf.shape(dist1)[0], -1]), axis=1)  # sum over all dims, except 0
    print(dist1)
    if dim_less:
        dim1 = tf.cast(tf.math.divide(tf.size(x1), tf.shape(x1)[0]), dtype=tf.float32)
        dist1 = tf.math.divide(dist1, dim1)  # divide by input dimension
    return tf.stack((dist1, dist1), axis=1)


if __name__ == "__main__":
    x1 = tf.constant([[[1., 1.], [1., 1.]], [[1., 1.], [1., 1.]]])
    x2 = tf.constant([[[2., 2.], [2., 2.]], [[2., 2.], [2., 2.]]])
    print(call_t(x1, x2, dim_less=False).numpy())
    print(call_t(x1, x2, dim_less=True).numpy())
