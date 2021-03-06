""" Define alexnet model. """
from keras.layers import Conv2D, MaxPooling2D, Input, Flatten, Dense
from keras.models import Model


def conv(layer, filters, kernal, activation='relu', pooling=True, stride=(1, 1)):
    """
        This defines single CNN layer in deep neural network.

        Args:
            layer: Previous layer appended to current layer.
            filters: Filter (channel) size of next layer.
            kernal: Kernal size of CNN layer.
            activation: Activation function.
            pooling: Define if this block needs max-pooling layer.
            stride: Stride size.

        Returns:
            Conv2D: Keras CNN layer appended with input.
    """
    if pooling:
        layer = MaxPooling2D(strides=(2, 2), pool_size=(2, 2))(layer)
    layer = Conv2D(filters, kernel_size=kernal, activation=activation,
                   strides=stride, padding='same')(layer)
    return layer


def block1():
    """ CNN block in alexnet. """
    image = Input(shape=(224, 224, 3))

    layer = conv(image, 48, (11, 11), pooling=False, stride=(4, 4))
    layer = conv(layer, 128, (5, 5))

    layer = conv(layer, 192, (3, 3))
    layer = conv(layer, 192, (3, 3), pooling=False)
    layer = conv(layer, 128, (3, 3), pooling=False)

    layer = MaxPooling2D(strides=(2, 2), pool_size=(2, 2))(layer)
    layer = Flatten()(layer)
    return Model(image, layer)


def fc1():
    """ First separated fully connected layer. """
    block_input = Input(shape=(6272,))
    layer = Dense(2048, activation='relu')(block_input)
    return Model(block_input, layer)


def fc2():
    """ Second fully connected layer. """
    block_input = Input(shape=(4096,))
    layer = Dense(4096, activation='relu')(block_input)
    layer = Dense(1000, activation='softmax')(layer)
    return Model(block_input, layer)