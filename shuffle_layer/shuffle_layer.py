import numpy as np
import tensorflow as tf


def channel_shuffle(l, groups):
    b, c, h, w = l.shape
    assert c % groups == 0, c # 必須被整除 need divide properly
    l = tf.reshape(l, [-1, c // groups, groups, h, w])
    l = tf.transpose(l, [0, 2, 1, 3, 4])

    l = tf.reshape(l, [b, c, h, w])
    return l



if __name__ == "__main__":
    zeros = np.zeros([2,3,3])
    ones = np.ones([2,3,3])
    twos = np.ones([2,3,3]) * 2
    input = np.concatenate([zeros, ones, twos]).reshape(1, 6, 3, 3)
    print(channel_shuffle(input, 2)[0], input)