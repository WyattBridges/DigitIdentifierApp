import numpy as np
import tensorflow as tf
import keras
from keras.datasets import mnist

# function to load the MNIST handwritten digits dataset as flattened examples
def load_mnist_flattened():
    # Load, reshape, and scale the dataset
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    x_train = x_train.reshape(len(x_train), 28*28)
    x_test = x_test.reshape(len(x_test), 28*28)
    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')
    x_train /= 255
    x_test /= 255
    num_classes = 10
    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)

    return (x_train, y_train), (x_test, y_test)

# Function to load the MNIST handwritten digits as 28-by-28 square images, for convolutional neural network architectures
def load_mnist_square():
    # Load, reshape, and scale the dataset
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    x_train = np.reshape(x_train, [-1, 28, 28, 1])
    x_test = np.reshape(x_test, [-1, 28, 28, 1])

    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')
    x_train /= 255
    x_test /= 255
    num_classes = 10
    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)

    return (x_train, y_train), (x_test, y_test)

# Function to load the MNIST handwritten digits as 32-by-32 square images, to be compatible with the LeNet-5 architecture
def load_mnist_square_32x32():
    # Load, reshape, and scale the dataset
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    x_train = np.reshape(x_train, [-1, 28, 28])
    x_test = np.reshape(x_test, [-1, 28, 28])

    # Each example must have 3 dimensions (height, width, channels) and be 32-by-32
    x_train = np.pad(x_train, ((0,0), (2,2), (2, 2)), 'constant')
    x_test = np.pad(x_test, ((0,0), (2,2), (2, 2)), 'constant')
    x_train = np.reshape(x_train, [-1, 32, 32, 1])
    x_test = np.reshape(x_test, [-1, 32, 32, 1])

    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')
    x_train /= 255
    x_test /= 255
    num_classes = 10
    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)

    return (x_train, y_train), (x_test, y_test)
