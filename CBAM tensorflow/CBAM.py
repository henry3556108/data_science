from tensorflow.keras import layers
import tensorflow as tf
from tensorflow.keras import regularizers
import numpy as np

class ChannelAttention(layers.Layer):
    def __init__(self, concat, ratio=16):
        super(ChannelAttention, self).__init__()
        self.avg_out= layers.GlobalAveragePooling2D()
        self.max_out= layers.GlobalMaxPooling2D()
        # shared for both inputs, and the ReLU activation function is followed by W0, compress then expend
        self.sharMLP = tf.keras.Sequential(
            [layers.Dense(concat//ratio, kernel_initializer='he_normal',
                kernel_regularizer=regularizers.l2(),
                activation=tf.nn.relu),
            layers.Dense(concat, kernel_initializer='uniform',
                kernel_regularizer=regularizers.l2())
            ]
        )

    def call(self, inputs):
        avg_out = self.avg_out(inputs)
        max_out = self.max_out(inputs)
        out = tf.stack([avg_out, max_out], axis=1)  # shape=(None, 2, fea_num)
        out = self.sharMLP(out)
        out = tf.reduce_sum(out, axis=1)      		# shape=(None, 16)
        out = tf.nn.sigmoid(out)
        out = layers.Reshape((1, 1, out.shape[1]))(out) # out.shape[0] = batch size
        return out


class SpatialAttention(layers.Layer):
    def __init__(self, kernel_size=7):
        super(SpatialAttention, self).__init__()
        self.conv1 = layers.Conv2D(1, kernel_size, strides=1, padding='same',name='spatial_conv2d')

    def call(self, inputs):
        avg_out = tf.reduce_mean(inputs, axis=3, keepdims=True, name='spatial_avgpool')
        max_out = tf.reduce_max(inputs, axis=3, keepdims=True, name='spatial_maxpool')
        out = tf.concat([avg_out, max_out], axis=3)
        out = self.conv1(out)
        out = tf.nn.sigmoid(out)
        return out

class CBAM(layers.Layer):
    def __init__(self, channels, reduction_ratio = 16):
        super(CBAM, self).__init__()
        self.C_layer = ChannelAttention(channels, reduction_ratio)
        self.S_layer = SpatialAttention()
    def call(self, input):
        channel_out = self.C_layer(input)
        cbam_out = self.S_layer(channel_out)
        return cbam_out


if __name__ == "__main__":
    input=tf.keras.layers.Input(shape=(128,128,16))
    output=CBAM(16)(input)
    m=tf.keras.models.Model(input,output)
    m.summary()