
from saphyra import *
import tensorflow as tf
from tensorflow.keras import layers



input  = layers.Input(shape=(1,), name = 'Input')
output = layers.Dense(1)(input)
model  = tf.keras.Model(input, output, name = "dummy")



create_jobs( models = [model],
        nInits        = 2,
        nInitsPerJob  = 1,
        sortBounds    = 10,
        nSortsPerJob  = 1,
        nModelsPerJob = 1,
        outputFolder  = 'job_config.Zee_v1_el.10sorts.2inits' )


