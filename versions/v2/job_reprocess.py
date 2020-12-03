#!/usr/bin/env python


def getPatterns( path, cv, sort):

  import numpy as np
  # Load data
  from Gaugi import load
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


  # Fix all shower shapes variables
  print( 'eratio > [10,inf[ = %d'%len(data_eratio[data_eratio>10.0]) )
  data_eratio[data_eratio>10.0]=-1
  print( 'eratio > [1,10[ = %d'%len(data_eratio[data_eratio>1.0]) )
  data_eratio[data_eratio>1.]=1.0
  print ('wstor < -99 =  %d'%len(data_wstot[data_wstot<-99]))
  data_wstot[data_wstot<-99]=-1



  target = d['target']
  target[target!=1]=-1


  # This is mandatory
  splits = [(train_index, val_index) for train_index, val_index in cv.split(data_reta,target)]

  data_shower_shapes = np.concatenate( (data_reta,data_eratio,data_f1,data_f3,data_weta2, data_wstot), axis=1)

    # split for this sort
  x_train = data_shower_shapes [ splits[sort][0] ]
  x_val   = data_shower_shapes [ splits[sort][1] ]
  y_train = target [ splits[sort][0] ]
  y_val   = target [ splits[sort][1] ]

  return x_train, x_val, y_train, y_val, splits



import argparse
import sys,os


parser = argparse.ArgumentParser(description = '', add_help = False)
parser = argparse.ArgumentParser()


parser.add_argument('-f','--tunedFile', action='store',
        dest='tunedFile', required = True,
            help = "The tuned file to be reprocess.")

parser.add_argument('-v','--volume', action='store',
        dest='volume', required = True, default = None,
            help = "The volume.")

parser.add_argument('-d','--dataFile', action='store',
        dest='dataFile', required = True, default = None,
            help = "The data file used to train the model.")

parser.add_argument('-r','--refFile', action='store',
        dest='refFile', required = True, default = None,
            help = "The reference file.")


if len(sys.argv)==1:
  parser.print_help()
  sys.exit(1)

args = parser.parse_args()

try:

  targets = [
                ('tight_cutbased' , 'T0HLTElectronT2CaloTight'        ),
                ('medium_cutbased', 'T0HLTElectronT2CaloMedium'       ),
                ('loose_cutbased' , 'T0HLTElectronT2CaloLoose'        ),
                ('vloose_cutbased', 'T0HLTElectronT2CaloVLoose'       ),
                ]
  
  
  from saphyra.decorators import Summary, Reference
  decorators = [Summary(), Reference(args.refFile, targets)]
  
  from sklearn.model_selection import StratifiedKFold
  from saphyra.applications import BinaryClassificationJob
  
  cv = StratifiedKFold(n_splits=10, random_state=512, shuffle=True)
  
  from saphyra import PatternGenerator
  from saphyra.utils import reprocess
  
  reprocess( PatternGenerator( args.dataFile, getPatterns), args.tunedFile, args.volume, cv, decorators )


  # necessary to work on orchestra
  from saphyra import lock_as_completed_job
  lock_as_completed_job(args.volume if args.volume else '.')

  sys.exit(0)

except  Exception as e:
  print(e)

  # necessary to work on orchestra
  from saphyra import lock_as_failed_job
  lock_as_failed_job(args.volume if args.volume else '.')

  sys.exit(1)





