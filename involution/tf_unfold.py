import tensorflow as tf

def involution_unfold_4d(x, kernel_size=3, stride=1, group=1):
    B, W, H, C = x.shape
    x = tf.compat.v1.extract_image_patches(x, ksizes=[1,kernel_size, kernel_size,1], strides=[1, stride, stride, 1], rates=[1,1,1,1], padding="SAME")
    x = tf.reshape(x, [B,H//stride,W//stride,kernel_size*kernel_size,C//group,group])
    return x