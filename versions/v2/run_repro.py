
import os

tunedFile  = '~/tasks/user.jodafons.data17_13TeV.AllPeriods.sgn.probes_lhmedium_EGAM1.bkg.VProbes_EGAM7.GRL_v97.v2_et{ET}_eta{ETA}.r1'
outputFile = 'user.jodafons.data17_13TeV.AllPeriods.sgn.probes_lhmedium_EGAM1.bkg.VProbes_EGAM7.GRL_v97.v2_et{ET}_eta{ETA}.r2'
refFile    = '~/cern_data/data/files/Zee/data17_13TeV.AllPeriods.sgn.probes_lhmedium_EGAM1.bkg.VProbes_EGAM7.GRL_v97/references/data17_13TeV.AllPeriods.sgn.probes_lhmedium_EGAM1.bkg.VProbes_EGAM7.GRL_v97_et{ET}_eta{ETA}.ref.pic.gz'
dataFile   = '~/cern_data/data/files/Zee/data17_13TeV.AllPeriods.sgn.probes_lhmedium_EGAM1.bkg.VProbes_EGAM7.GRL_v97/data17_13TeV.AllPeriods.sgn.probes_lhmedium_EGAM1.bkg.VProbes_EGAM7.GRL_v97_et{ET}_eta{ETA}.npz'



command = "python job_reprocess.py -d {DATA} -r {REF} -o {OUT} -t {IN}"


for et in range(5):
    for eta in range(5):

        cmd = command.format( DATA=dataFile.format(ET=et,ETA=eta) , REF=refFile.format(ET=et,ETA=eta), IN=tunedFile.format(ET=et,ETA=eta), OUT=outputFile.format(ET=et,ETA=eta) )
        print(cmd)

        os.system(cmd)

