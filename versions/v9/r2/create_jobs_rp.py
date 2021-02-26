

from saphyra import *
from saphyra import RpLayer
from tensorflow.keras.layers import Layer
import tensorflow as tf

def get_model(rvec):
  modelCol = []
  from tensorflow.keras.models import Sequential
  from tensorflow.keras.layers import Dense, Dropout, Activation, Conv1D, Flatten
  for n in range(2,5+1):
    model = Sequential()
    layerRp = Rplayer(rvec)
    inputRp = layerRp.build(100)
    model.add(inputRp)
    model.add(Dense(n, input_shape=(100,), activation='tanh', name='dense_layer'))
    model.add(Dense(1, activation='linear', name='output_for_inference'))
    model.add(Activation('tanh', name='output_for_training'))
    modelCol.append(model)
  return modelCol

rvec = np.concatenate((np.arange(1,9),np.arange(1,65),np.arange(1,9),np.arange(1,9),np.arange(1,5),np.arange(1,5),np.arange(1,5)))

create_jobs( models = get_model(),
        nInits        = 10,
        nInitsPerJob  = 1,
        sortBounds    = 10,
        nSortsPerJob  = 1,
        nModelsPerJob = 1,
        outputFolder  = 'job_config.Zee_v8.n2to5.10sorts.10inits.r0' )


