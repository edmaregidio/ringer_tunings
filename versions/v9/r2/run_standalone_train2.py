import os
import glob

from itertools import product

# define the paths into the container
data_path = '/home/edmar.egidio/datasets/npz/NPZ/dataset17_13TeV/data17_13TeV.AllPeriods.sgn.probes_lhmedium_EGAM1.bkg.VProbes_EGAM7.GRL_v97_et%i_eta%i.npz'
ref_path = '/home/edmar.egidio/Tunings/RingerRp/r1/ref/data17_13TeV.AllPeriods.sgn.probes_lhmedium_EGAM1.bkg.VProbes_EGAM7.GRL_v97_et%i_eta%i.ref.pic.gz'
config_path = '/home/edmar.egidio/Tunings/RingerRp/r1/config/job_config.Zee_Rp.2n10.10sorts.10inits.r1/*'
output_path = '/home/edmar.egidio/Tunings/RingerRp/r1/output_rp/user.eegidiop.data17_13TeV.AllPeriods.sgn.probes_lhmedium_EGAM1.bkg.VProbes_EGAM7.GRL_v97_et%i_eta%i.rp.r1'

# create a list of config files
config_list  = glob.glob(config_path)
print(config_list)


# loop over the bins
for iet, ieta in product(range(2,5), range(0,5)):
    print('Processing -> et: %i | eta: %i' %(iet, ieta))
    # format the names
    data_file = data_path %(iet, ieta)
    ref_file  = ref_path  %(iet, ieta)
    out_name  = output_path %(iet, ieta)

    # loop over the config files
    for iconfig in config_list:
        m_command = """python3 job_tuning_rp.py -c {CONFIG} \\
                       -d {DATAIN} \\
                       -v {OUT} \\
                       -r {REF}""".format(CONFIG=iconfig, DATAIN=data_file, OUT=out_name, REF=ref_file)

        print(m_command)
        # execute the tuning
        os.system(m_command)
