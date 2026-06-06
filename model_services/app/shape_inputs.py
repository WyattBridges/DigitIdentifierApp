import numpy as np
import tensorflow as tf

# function for shaping and scaling inputs in preparation for models that accept flattened inputs
def flatten_inputs(x):
    x = x.reshape(len(x), 28*28)
    x = x.astype('float32')
    x /= 255
    return x

# function for shaping and scaling inputs in preparation for models that accept 28-by-28 grayscale images
def inputs_as_square(x):
    x = np.reshape(x, [-1, 28, 28, 1])
    x = x.astype('float32')
    x /= 255
    return x

# function for shaping and scaling inputs in preparation for models that accept 32-by-32 grayscale images
def inputs_as_square_32x32(x):
    x = np.reshape(x, [-1, 28, 28])
    x = np.pad(x, ((0,0), (2,2), (2, 2)), 'constant')
    x = np.reshape(x, [-1, 32, 32, 1])
    x = x.astype('float32')
    x /= 255
    return x
