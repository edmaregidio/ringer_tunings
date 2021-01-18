
from saphyra import *
import tensorflow as tf
from tensorflow.keras import layers

# rings
input_rings = layers.Input(shape=(100,), name='Input_rings')
conv_rings   = layers.Reshape((100,1))(input_rings)
#conv_rings   = layers.Conv1D( 16, kernel_size=2, name='conv1d_rings_1', activation='relu')(conv_rings)
conv_rings   = layers.Conv1D( 4, kernel_size=2, name='conv1d_rings_1', activation='relu')(conv_rings)
#conv_rings   = layers.Conv1D( 32, kernel_size=2, name='conv1d_rings_2', activation='relu')(conv_rings)
conv_rings   = layers.Conv1D( 8, kernel_size=2, name='conv1d_rings_2', activation='relu')(conv_rings)
conv_output  = layers.Flatten()(conv_rings)
#dense_from_conv = layers.Dense(32, activation='relu', name='dense_conv_layer')(conv_output)

# shower shapes
input_shower_shapes = layers.Input(shape=(6,), name='Input_shower_shapes')
dense_shower_shapes = layers.Dense(5, activation='relu', name='dense_shower_layer')(input_shower_shapes)

# decision layer
#input_concat = layers.Concatenate(axis=1)([dense_from_conv, dense_shower_shapes])
input_concat = layers.Concatenate(axis=1)([conv_output, dense_shower_shapes])

dense = layers.Dense(16, activation='relu', name='dense_layer')(input_concat)
dense = layers.Dense(1,activation='linear', name='output_for_inference')(dense)
#dense = layers.Dense(1,activation='linear', name='output_for_inference', kernel_regularizer='l2', bias_regularizer='l2')(dense)
output = layers.Activation('sigmoid', name='output_for_training')(dense)


# Build the model
model = tf.keras.Model([input_rings, input_shower_shapes], output, name = "model")


input  = layers.Input(shape=(1,), name = 'Input')
output = layers.Dense(1)(input)
model  = tf.keras.Model(input, output, name = "dummy")

create_jobs( models = [model],
        nInits        = 10,
        nInitsPerJob  = 1,
        sortBounds    = 10,
        nSortsPerJob  = 1,
        nModelsPerJob = 1,
        outputFolder  = 'job_config.Zee_v11.10sorts.10inits.r0' )


