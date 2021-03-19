import os
import glob

from itertools import product

# define the paths into the container
data_path    = '/eos/user/e/eegidiop/Derivations/NPZ/NPZ1/dataset17_13TeV/data17_13TeV.AllPeriods.sgn.probes_lhmedium_EGAM1.bkg.VProbes_EGAM7.GRL_v97_et%i_eta%i.npz'
ref_path     = '/eos/user/e/eegidiop/RingerDev/Tunings/RingerRp/r0/ref/edmar.egidio/Tunings/v9/RingerRp/ref/data17_13TeV.AllPeriods.sgn.probes_lhmedium_EGAM1.bkg.VProbes_EGAM7.GRL_v97_et%i_eta%i.ref.pic.gz'
config_path  = '/eos/user/e/eegidiop/RingerDev/Tunings/RingerRp/r0/config/job_config.Zee_Rp.n5.10sorts.5inits.r0/*'
output_path  = '/eos/user/e/eegidiop/RingerDev/Tunings/RingerRp/r0/output/user.eegidiop.data17_13TeV.AllPeriods.sgn.probes_lhmedium_EGAM1.bkg.VProbes_EGAM7.GRL_v97_et%i_eta%i.v9.r2'

# create a list of config files
config_list  = glob.glob(config_path)
print(config_list)

# loop over the bins
for iet, ieta in product(range(0,1), range(0,1)):
    print('Processing -> et: %i | eta: %i' %(iet, ieta))
    # format the names
    data_file = data_path %(iet, ieta)
    ref_file  = ref_path  %(iet, ieta)
    out_name  = output_path %(iet, ieta)

    # loop over the config files
    for iconfig in config_list:
        m_command = """python3 /afs/cern.ch/user/e/eegidiop/ringerdev/git_repos/ringer_tunings/versions/v9/r2/job_tuning_rp.py -c {CONFIG} \\
                       -d {DATAIN} \\
                       -v {OUT} \\
                       -r {REF}""".format(CONFIG=iconfig, DATAIN=data_file, OUT=out_name, REF=ref_file)

        print(m_command)
        # execute the tuning
        os.system(m_command)
