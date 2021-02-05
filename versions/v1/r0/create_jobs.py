from saphyra import *

# tensorflow
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Conv1D, Flatten

# function to define the keras model
def get_model(neuron_min, neuron_max):
  modelCol = []
  for n in range(neuron_min,neuron_max+1):
    model = Sequential()
    model.add(Dense(n, input_shape=(100,), activation='tanh', name='dense_layer'))
    model.add(Dense(1, activation='linear', name='output_for_inference'))
    model.add(Activation('tanh', name='output_for_training'))
    modelCol.append(model)
  return modelCol

# cross-validation method
n_folds = 10 # normally 10 folds

n_min_neuron = 2
n_max_neuron = 10
n_inits      = 10

create_jobs( 
        models       = get_model(neuron_min=n_min_neuron,
                                 neuron_max=n_max_neuron),
        nInits        = 5,
        nInitsPerJob  = 1,
        sortBounds    = 10,
        nSortsPerJob  = 1,
        nModelsPerJob = 5,
        outputFolder  = 'job_config.Zrad_v1.n2to10.10sorts.10inits.r0',
        )
