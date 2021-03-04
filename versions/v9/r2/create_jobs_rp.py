

from saphyra import *
from saphyra import RpLayer
from tensorflow.keras.layers import Layer
import tensorflow as tf
from tensorflow.keras import layers

inputs = layers.Input(shape=(100,), name='Input_rings')
input_rp = RpLayer()(inputs)
dense_rp = layers.Dense(5, activation='tanh', name='dense_rp_layer')(input_rp)
dense = layers.Dense(1,activation='linear', name='output_for_inference')(dense_rp)
outputs = layers.Activation('tanh', name='output_for_training')(dense)
model = tf.keras.Model(inputs, outputs, name = "model")


create_jobs( models = [model],
        nInits        = 5,
        nInitsPerJob  = 1,
        sortBounds    = 10,
        nSortsPerJob  = 1,
        nModelsPerJob = 1,
        outputFolder  = 'job_config.Zee_Rp.n5.10sorts.5inits.r0' )


