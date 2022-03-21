from operator import inv
from tensorflow.keras import layers
import tensorflow as tf
from tensorflow.keras import regularizers
import numpy as np
import tf_unfold

class Involution(layers.Layer):
    def __init__(self, channel=4, group_number=2, kernel_size=3, stride=2, reduction_ratio=1):
        super().__init__()
        assert reduction_ratio <= channel, print("Reduction ration must be less than or equal to channel size")
        assert channel % group_number == 0 , print("channel must be divisible by group_number")        
        self.channel = channel
        self.group_number = group_number
        self.kernel_size = kernel_size
        self.stride = stride
        self.reduction_ratio = reduction_ratio
        self.avgpool = tf.keras.layers.AveragePooling2D(
            pool_size=self.stride,
            strides=self.stride,
            padding="same") if self.stride > 1 else tf.identity
        self.conv1 = tf.keras.layers.Conv2D(
                filters=self.channel//self.reduction_ratio, # 
                kernel_size=1)
        self.conv2 = tf.keras.layers.Conv2D(
            filters=self.group_number*self.kernel_size*self.kernel_size,
            kernel_size=1
        )
        self.sequence = tf.keras.Sequential(
            [self.avgpool,
            self.conv1,
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.ReLU(),
            self.conv2]    
        )
    def call(self, x):
        B, H, W, C = x.shape
        weight = self.sequence(x)
        unfold_x = tf_unfold.involution_unfold_4d(x, kernel_size=3, stride=self.stride, group=self.group_number)
        reshape_weight = tf.reshape(weight, [B, H//self.stride, W//self.stride, self.kernel_size*self.kernel_size, 1, self.group_number])
        out = tf.math.multiply(reshape_weight, unfold_x)                              # B, H, W, K*K, C//G, G
        out = tf.math.reduce_sum(out, axis=3) 
        out = tf.reshape(out, [B, H // self.stride, W // self.stride, C])   
        return out

if __name__=="__main__":
    x = np.random.rand(1,4,4,4)
    involution = Involution(group_number=1)
    out = involution(x)
    print(out.shape)
