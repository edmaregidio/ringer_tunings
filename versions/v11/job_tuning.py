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


from Gaugi import load
from Gaugi.messenger.macros import *
from saphyra.utils import model_generator_base
import numpy as np
import argparse
import sys,os


parser = argparse.ArgumentParser(description = '', add_help = False)
parser = argparse.ArgumentParser()


parser.add_argument('-c','--configFile', action='store',
        dest='configFile', required = True,
            help = "The job config file that will be used to configure the job (sort and init).")

parser.add_argument('-v','--volume', action='store',
        dest='volume', required = False, default = None,
            help = "The volume output.")

parser.add_argument('-d','--dataFile', action='store',
        dest='dataFile', required = True, default = None,
            help = "The data/target file used to train the model.")

parser.add_argument('-r','--refFile', action='store',
        dest='refFile', required = True, default = None,
            help = "The reference file.")

parser.add_argument('-t','--type', action='store',
        dest='type', required = True, default = 'fusion',
            help = "The type of derivation (ringer, shower or fusion)")

parser.add_argument('--path_to_v10', action='store',
        dest='path_to_v10', required = False, default = None,
            help = "The path to the ringer v10 tuned files.")

parser.add_argument('--path_to_v9_ss', action='store',
        dest='path_to_v9_ss', required = False, default = None,
            help = "The path to the v9 shower tuned files.")


if len(sys.argv)==1:
  parser.print_help()
  sys.exit(1)


args = parser.parse_args()



#
# Get shower shapes patterns from file
#
def getPatterns_shower( path, cv, sort):

  d = load(path)
  feature_names = d['features'].tolist()

  # How many events?
  n = d['data'].shape[0]

  # extract all shower shapes
  data_reta   = d['data'][:, feature_names.index('L2Calo_reta')].reshape((n,1)) / 1.0
  data_eratio = d['data'][:, feature_names.index('L2Calo_eratio')].reshape((n,1)) / 1.0
  data_f1     = d['data'][:, feature_names.index('L2Calo_f1')].reshape((n,1)) / 0.6
  data_f3     = d['data'][:, feature_names.index('L2Calo_f3')].reshape((n,1)) / 0.04
  data_weta2  = d['data'][:, feature_names.index('L2Calo_weta2')].reshape((n,1)) / 0.02
  data_wstot  = d['data'][:, feature_names.index('L2Calo_wstot')].reshape((n,1)) / 1.0

  target = d['target']

  # Fix all shower shapes variables
  data_eratio[data_eratio>10.0]=0
  data_eratio[data_eratio>1.]=1.0
  data_wstot[data_wstot<-99]=0

  # This is mandatory
  splits = [(train_index, val_index) for train_index, val_index in cv.split(data_reta,target)]

  data_shower = np.concatenate( (data_reta,data_eratio,data_f1,data_f3,data_weta2, data_wstot), axis=1)

  # split for this sort
  x_train = [ data_shower[splits[sort][0]] ]
  x_val   = [ data_shower[splits[sort][1]] ]
  y_train = target [ splits[sort][0] ]
  y_val   = target [ splits[sort][1] ]

  return x_train, x_val, y_train, y_val, splits, []



#
# Get ringer shape from file
#
def getPatterns_rings( path, cv, sort):

  def norm1( data ):
      norms = np.abs( data.sum(axis=1) )
      norms[norms==0] = 1
      return data/norms[:,None]

  d = load(path)
  data = norm1(d['data'][:,1:101])


  target = d['target']
  splits = [(train_index, val_index) for train_index, val_index in cv.split(data,target)]
  x_train = data [ splits[sort][0]]
  y_train = target [ splits[sort][0] ]
  x_val = data [ splits[sort][1]]
  y_val = target [ splits[sort][1] ]

  return x_train, x_val, y_train, y_val, splits, []





#
# Get shower shapes patterns from file
#
def getPatterns_fusion( path, cv, sort):


  def norm1( data ):
      norms = np.abs( data.sum(axis=1) )
      norms[norms==0] = 1
      return data/norms[:,None]

  d = load(path)
  feature_names = d['features'].tolist()
  
  # How many events?
  n = d['data'].shape[0]

  # extract all rings
  data_rings  = norm1(d['data'][:,1:101])
  # extract all shower shapes
  data_reta   = d['data'][:, feature_names.index('L2Calo_reta')].reshape((n,1)) / 1.0
  data_eratio = d['data'][:, feature_names.index('L2Calo_eratio')].reshape((n,1)) / 1.0
  data_f1     = d['data'][:, feature_names.index('L2Calo_f1')].reshape((n,1)) / 0.6
  data_f3     = d['data'][:, feature_names.index('L2Calo_f3')].reshape((n,1)) / 0.04
  data_weta2  = d['data'][:, feature_names.index('L2Calo_weta2')].reshape((n,1)) / 0.02
  data_wstot  = d['data'][:, feature_names.index('L2Calo_wstot')].reshape((n,1)) / 1.0

  target = d['target']

  # Fix all shower shapes variables
  data_eratio[data_eratio>10.0]=0
  data_eratio[data_eratio>1.]=1.0
  data_wstot[data_wstot<-99]=0

  # This is mandatory
  splits = [(train_index, val_index) for train_index, val_index in cv.split(data_reta,target)]

  data_shower = np.concatenate( (data_reta,data_eratio,data_f1,data_f3,data_weta2, data_wstot), axis=1)

  # split for this sort
  x_train = [ data_rings[splits[sort][0]], data_shower[splits[sort][0]] ]
  x_val   = [ data_rings[splits[sort][1]], data_shower[splits[sort][1]] ]
  y_train = target [ splits[sort][0] ]
  y_val   = target [ splits[sort][1] ]

  return x_train, x_val, y_train, y_val, splits, []




#
# Get configuration file
#
def getJobConfigId( path ):
  return dict(load(path))['id']





#
# Model generator
#
class Model( model_generator_base ):

  def __init__( self, v10_path, v9_ss_path ):

    model_generator_base.__init__(self)
    import tensorflow as tf
    from tensorflow.keras import layers
   

    # rings
    input_rings = layers.Input(shape=(100,), name='Input_rings')
    conv_rings   = layers.Reshape((100,1))(input_rings)
    #conv_rings   = layers.Conv1D( 16, kernel_size=2, name='conv1d_rings_1', activation='relu')(conv_rings)
    conv_rings   = layers.Conv1D( 4, kernel_size=3, name='conv1d_rings_1', activation='relu')(conv_rings)
    #conv_rings   = layers.Conv1D( 32, kernel_size=2, name='conv1d_rings_2', activation='relu')(conv_rings)
    conv_rings   = layers.Conv1D( 8, kernel_size=3, name='conv1d_rings_2', activation='relu')(conv_rings)
    conv_output  = layers.Flatten()(conv_rings)
    #dense_from_conv = layers.Dense(32, activation='relu', name='dense_conv_layer')(conv_output)
    
    # shower shapes
    input_shower_shapes = layers.Input(shape=(6,), name='Input_shower_shapes')
    dense_shower_shapes = layers.Dense(5, activation='relu', name='dense_shower_layer')(input_shower_shapes)
    
    
    # decision layer
    #input_concat = layers.Concatenate(axis=1)([dense_from_conv, dense_shower_shapes])
    input_concat = layers.Concatenate(axis=1)([conv_output, dense_shower_shapes])

    dense = layers.Dense(16, activation='relu', name='dense_layer')(input_concat)
    #dense = layers.Dense(1,activation='linear', name='output_for_inference')(dense)
    dense = layers.Dense(1,activation='linear', name='output_for_inference', kernel_regularizer='l2', bias_regularizer='l2')(dense)
    output = layers.Activation('sigmoid', name='output_for_training')(dense)


    # Build the model
    self.__model = tf.keras.Model([input_rings, input_shower_shapes], output, name = "model")
    self.__tuned_v10_models = self.load_models(v10_path)
    self.__tuned_v9_ss_models = self.load_models(v9_ss_path)

 
    # Follow the strategy proposed by werner were we keep these weights free to do the fine tunings
    # since most part of these variables have an stronge relationship (correlation).
    self.__trainable=True
    #self.__trainable=False



  #
  # Make the fusion
  #
  def __call__( self, sort ):

    print('aki joao')
    from tensorflow.keras.models import clone_model
    # create a new model
    model = clone_model( self.__model )
    MSG_INFO(self, "Target model:" )
    model.summary()
    
    v10 = self.get_best_model( self.__tuned_v10_models, sort , 0) # five neurons in the hidden layer
    MSG_INFO( self, "v10 model (right):")
    v10.summary()
    
    v9_ss = self.get_best_model( self.__tuned_v9_ss_models, sort , 0) # five neurons in the hidden layer
    MSG_INFO( self, "v9 model (left):")
    v9_ss.summary()

    self.transfer_weights( v10  , 'conv1d_layer_1' , model, 'conv1d_rings_1'        , trainable=self.__trainable)
    self.transfer_weights( v10  , 'conv1d_layer_2' , model, 'conv1d_rings_2'        , trainable=self.__trainable)
    self.transfer_weights( v10  , 'dense_layer'  , model, 'dense_conv_layer'  , trainable=self.__trainable)
    self.transfer_weights( v9_ss, 'dense_layer'  , model, 'dense_shower_layer'  , trainable=self.__trainable)
    return model



try:


  
  job_id = getJobConfigId( args.configFile )

  outputFile = args.volume+'/tunedDiscr.jobID_%s'%str(job_id).zfill(4) if args.volume else 'test.jobId_%s'%str(job_id).zfill(4)

  targets = [
                ('tight_cutbased' , 'T0HLTElectronT2CaloTight'        ),
                ('medium_cutbased', 'T0HLTElectronT2CaloMedium'       ),
                ('loose_cutbased' , 'T0HLTElectronT2CaloLoose'        ),
                ('vloose_cutbased', 'T0HLTElectronT2CaloVLoose'       ),
                ]


  from saphyra.callbacks import sp
  from saphyra import PatternGenerator
  from sklearn.model_selection import StratifiedKFold
  from saphyra.applications import BinaryClassificationJob
  from saphyra.decorators import Summary, Reference
  from saphyra.utils.plot_generator import plot_training_curves

  # create decorators
  decorators = [Summary(), Reference(args.refFile, targets)]


  model = None
  # Select the correct pattern
  if args.type == 'shower':
    getPatterns=getPatterns_shower
  elif args.type == 'rings':
    getPatterns=getPatterns_rings
  elif args.type == 'fusion':
    getPatterns=getPatterns_fusion
    model = Model( args.path_to_v10, args.path_to_v9_ss )
  else:
    getPatterns=getPatterns_rings


  #
  # Create the binary job
  #
  job = BinaryClassificationJob(  PatternGenerator( args.dataFile, getPatterns ),
                                  StratifiedKFold(n_splits=10, random_state=512, shuffle=True),
                                  job               = args.configFile,
                                  loss              = 'binary_crossentropy',
                                  metrics           = ['accuracy'],
                                  callbacks         = [sp(patience=25, verbose=True, save_the_best=True)],
                                  epochs            = 5000,
                                  class_weight      = False,
                                  model_generator   = model, # Force to work with model generator (Hack)
                                  models            = [None] if args.type=='fusion' else None, # Force to work with model generator (Hack)
                                  #plots             = [plot_training_curves],
                                  outputFile        = outputFile )

  job.decorators += decorators


  #
  # Run it!
  #
  job.run()


  # necessary to work on orchestra
  from saphyra import lock_as_completed_job
  lock_as_completed_job(args.volume if args.volume else '.')
  sys.exit(0)



except Exception as e:
  print(e)
  # necessary to work on orchestra
  from saphyra import lock_as_failed_job
  lock_as_failed_job(args.volume if args.volume else '.')
  sys.exit(1)



