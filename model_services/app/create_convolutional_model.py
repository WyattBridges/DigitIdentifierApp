import numpy as np
import tensorflow as tf
import keras
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten
from keras.optimizers import RMSprop
from load_mnist import *

# Load MNIST as square, 32-by-32 grayscale examples
(x_train, y_train), (x_test, y_test) = load_mnist_square_32x32()

# Build and compile the model, which is based on the LeNet-5 architecture
model_2 = Sequential()
model_2.add(Conv2D(filters=6, kernel_size=(5,5), strides=(1,1), input_shape=(32,32,1), padding='same', activation='relu'))
model_2.add(MaxPooling2D(pool_size=(2, 2), strides=(2,2)))
model_2.add(Conv2D(filters=16, kernel_size=(5,5), strides=(1,1), padding='same', activation='relu'))
model_2.add(MaxPooling2D(pool_size=(2, 2), strides=(2,2)))
model_2.add(Flatten())
model_2.add(Dense(120, activation = 'relu'))
model_2.add(Dense(84, activation = 'relu'))
model_2.add(Dense(10, activation = 'softmax'))
model_2.summary()

learning_rate = .001
model_2.compile(loss='categorical_crossentropy',
                optimizer=RMSprop(learning_rate=learning_rate),
                metrics=['accuracy'])
    
# Train the model
model_2.fit(x_train, y_train,
            batch_size=128,
            epochs=20,
            verbose=1,
            validation_data=(x_test, y_test))
    
# Save the trained model
model_2.save('models/convolutional_model.keras')
