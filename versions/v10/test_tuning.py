#!/usr/bin/env python

try:
  from tensorflow.compat.v1 import ConfigProto
  from tensorflow.compat.v1 import InteractiveSession

  config = ConfigProto()
  config.gpu_options.allow_growth = True
  session = InteractiveSession(config=config)
except Exception as e:
  print(e)
  print("Not possible to set gpu allow growth")



def getPatterns( path, cv, sort):

  def norm1( data ):
      norms = np.abs( data.sum(axis=1) )
      norms[norms==0] = 1
      return data/norms[:,None]

  from Gaugi import load
  import numpy as np
  d = load(path)
  data = norm1(d['data'][:,1:101])
  target = d['target']
  splits = [(train_index, val_index) for train_index, val_index in cv.split(data,target)]

  x_train = data [ splits[sort][0]]
  y_train = target [ splits[sort][0] ]
  x_val = data [ splits[sort][1]]
  y_val = target [ splits[sort][1] ]

  return x_train, x_val, y_train, y_val, splits, []


def getPileup( path ):
  from Gaugi import load
  return load(path)['data'][:,0]


def getJobConfigId( path ):
  from Gaugi import load
  return dict(load(path))['id']


import argparse
import sys,os


parser = argparse.ArgumentParser(description = '', add_help = False)
parser = argparse.ArgumentParser()



parser.add_argument('-d','--dataFile', action='store',
        dest='dataFile', required = True, default = None,
            help = "The data/target file used to train the model.")

parser.add_argument('-r','--refFile', action='store',
        dest='refFile', required = True, default = None,
            help = "The reference file.")


if len(sys.argv)==1:
  parser.print_help()
  sys.exit(1)

args = parser.parse_args()


# create the new model
from saphyra import *
import tensorflow as tf
from tensorflow.keras import layers


# expect an input with 100 domensions (features)
input = layers.Input(shape=(100,), name = 'Input') # 0
input_reshape = layers.Reshape((100,1), name='Reshape_layer')(input)
conv = layers.Conv1D(4, kernel_size = 2, activation='relu', name = 'conv1d_layer_1', kernel_regularizer=None)(input_reshape) # 1
#conv = layers.Dropout(0.2)(conv)
conv = layers.Conv1D(8, kernel_size = 2, activation='relu', name = 'conv1d_layer_2', kernel_regularizer=None)(conv) # 2
conv = layers.Flatten(name='flatten')(conv) # 3
dense = layers.Dense(8, activation='relu', name='dense_layer', kernel_regularizer=None, bias_regularizer=None)(conv) # 4
dense = layers.Dense(1,activation='linear', name='output_for_inference', kernel_regularizer='l2', bias_regularizer='l2')(dense) # 5
#dense = layers.Dense(1,activation='linear', name='output_for_inference')(dense) # 5
output = layers.Activation('sigmoid', name='output_for_training')(dense) # 6
model = tf.keras.Model(input, output, name = "model")




targets = [
              ('tight_cutbased' , 'T0HLTElectronT2CaloTight'        ),
              ('medium_cutbased', 'T0HLTElectronT2CaloMedium'       ),
              ('loose_cutbased' , 'T0HLTElectronT2CaloLoose'        ),
              ('vloose_cutbased', 'T0HLTElectronT2CaloVLoose'       ),
              ]


from saphyra.decorators import Summary, Reference
decorators = [Summary(), Reference(args.refFile, targets)]

from saphyra.callbacks import sp


from saphyra import PatternGenerator
from sklearn.model_selection import StratifiedKFold
from saphyra.applications import BinaryClassificationJob

from saphyra.utils.plot_generator import plot_training_curves

job = BinaryClassificationJob(  PatternGenerator( args.dataFile, getPatterns ),
                                StratifiedKFold(n_splits=10, random_state=512, shuffle=True),
                                sorts             = [0],
                                inits             = [0],
                                models            = [model],
                                loss              = 'binary_crossentropy',
                                metrics           = ['accuracy'],
                                callbacks         = [sp(patience=25, verbose=True, save_the_best=True)],
                                epochs            = 5000,
                                class_weight      = False,
                                plots             = [plot_training_curves],
                                outputFile        = 'test' )

job.decorators += decorators

# Run it!
job.run()


