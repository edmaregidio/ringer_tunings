
from saphyra import *
import tensorflow as tf
from tensorflow.keras import layers



input  = layers.Input(shape=(1,), name = 'Input')
output = layers.Dense(1)(input)
model  = tf.keras.Model(input, output, name = "dummy")


# ringer shape
input_rings = layers.Input(shape=(100,), name='Input_rings')
dense_rings = layers.Dense(5, activation='relu', name='dense_rings_layer')(input_rings)

# shower shapes
input_shower_shapes = layers.Input(shape=(6,), name='Input_shower_shapes')
dense_shower_shapes = layers.Dense(5, activation='relu', name='dense_shower_layer')(input_shower_shapes)

# track variables
input_track_variables = layers.Input(shape=(3,), name='Input_track_variables')
dense_track_variables = layers.Dense(5, activation='relu', name='dense_track_variables_layer')(input_track_variables)


# decision layer
input_concat = layers.Concatenate(axis=1)([dense_rings, dense_shower_shapes, dense_track_variables])
dense = layers.Dense(5, activation='relu', name='dense_layer')(input_concat)
dense = layers.Dense(1,activation='linear', name='output_for_inference')(dense)
output = layers.Activation('sigmoid', name='output_for_training')(dense)

   
model = tf.keras.Model([input_rings, input_shower_shapes, input_track_variables], output, name = "model")


create_jobs( models = [model],
        nInits        = 10,
        nInitsPerJob  = 1,
        sortBounds    = 10,
        nSortsPerJob  = 1,
        nModelsPerJob = 1,
        outputFolder  = 'job_config.Zee_v1_el.10sorts.10inits.r0' )


