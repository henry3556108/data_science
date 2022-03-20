import tensorflow as tf

def unfold_4d(x, ksizes=[1,3,3,1], strides=[1,1,1,1]):
    x = tf.compat.v1.extract_image_patches(x, ksizes=ksizes, strides=strides, rates=[1,1,1,1], padding="SAME")
    b,w,h,c = x.shape
    x = tf.reshape(x, [b, w*h, c])
    x = tf.transpose(x, perm=[0, 2, 1])
    return x