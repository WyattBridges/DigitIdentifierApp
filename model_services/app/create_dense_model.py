import numpy as np
import tensorflow as tf
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import RMSprop
from load_mnist import *

# Load MNIST as "flat" examples
(x_train, y_train), (x_test, y_test) = load_mnist_flattened()

# Build and compile the model
model_1 = Sequential()
model_1.add(Dense(128, activation='relu', input_shape=(784,)))
model_1.add(Dropout(0.5))
model_1.add(Dense(64, activation='relu'))
model_1.add(Dropout(0.5))
model_1.add(Dense(10, activation='softmax'))
model_1.summary()

learning_rate = .002
model_1.compile(loss='categorical_crossentropy',
                optimizer=RMSprop(learning_rate=learning_rate),
                metrics=['accuracy'])
    
# Train the model
model_1.fit(x_train, y_train,
            batch_size=128,
            epochs=30,
            verbose=1,
            validation_data=(x_test, y_test))
    
# Save the trained model
model_1.save('models/dense_model.keras')
