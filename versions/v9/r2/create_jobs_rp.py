

from saphyra import *
from saphyra import RpLayer
from tensorflow.keras.layers import Layer
import tensorflow as tf
from tensorflow.keras import layers

def get_model( ):
        modelCol = []
        for n in range(2,10+1):
                inputs = layers.Input(shape=(100,), name='Input_rings')
                input_rp = RpLayer()(inputs)
                dense_rp = layers.Dense(n, activation='tanh', name='dense_rp_layer')(input_rp)
                dense = layers.Dense(1,activation='linear', name='output_for_inference')(dense_rp)
                outputs = layers.Activation('tanh', name='output_for_training')(dense)
                model = tf.keras.Model(inputs, outputs, name = "model")
                modelCol.append(model)
        return modelCol

create_jobs( models = get_model(),
        nInits        = 10,
        nInitsPerJob  = 1,
        sortBounds    = 10,
        nSortsPerJob  = 1,
        nModelsPerJob = 1,
        outputFolder  = 'job_config.Zee_Rp.2n10.10sorts.10inits.r0' )


