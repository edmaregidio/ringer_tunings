import os
import glob

from itertools import product

# define the paths into the container
data_path    = '/home/juan/datasets/trigger/photons/npz/mc16_13TeV.sgn.probes_MC_DP.bkg.noMC.JF17_et%i_eta%i.npz'
ref_path     = '/home/juan/datasets/trigger/photons/ref/mc16_13TeV.sgn.probes_MC_DP.bkg.noMC.JF17_et%i_eta%i.ref.pic.gz'
config_path  = '/home/juan/datasets/trigger/photons/config/job_config.Zrad_v1.n2to10.10sorts.5inits/*'
output_path  = '/home/juan/datasets/trigger/photons/tunning/user.jlieberm.mc16_13TeV.sgn.probes_MC_DP.bkg.noMC.JF17_et%i_eta%i.v1'

# create a list of config files
config_list  = glob.glob(config_path)
print(config_list)

# loop over the bins
for iet, ieta in product(range(5), range(5)):
    print('Processing -> et: %i | eta: %i' %(iet, ieta))
    # format the names
    data_file = data_path %(iet, ieta)
    ref_file  = ref_path  %(iet, ieta)
    out_name  = output_path %(iet, ieta)

    # loop over the config files
    for iconfig in config_list:
        m_command = """python3 job_tuning.py -c {CONFIG} \\
                       -d {DATAIN} \\
                       -o {OUT} \\
                       -r {REF}""".format(CONFIG=iconfig, DATAIN=data_file, OUT=out_name, REF=ref_file)

        print(m_command)
        # execute the tuning
        os.system(m_command)
