import os
basepath = os.getcwd()

path = basepath + '/Zee/v11/r1'



# Path into the caloba cluster
path_to_rings  = '/home/jodafons/public/tunings/v10/user.jodafons.data17_13TeV.AllPeriods.sgn.probes_lhmedium_EGAM1.bkg.VProbes_EGAM7.GRL_v97.v10_et{ET}_eta{ETA}.r2/'
path_to_shower = '/home/jodafons/public/tunings/v9_ss/user.jodafons.data17_13TeV.AllPeriods.sgn.probes_lhmedium_EGAM1.bkg.VProbes_EGAM7.GRL_v97.v9_ss_et{ET}_eta{ETA}.r0/'

command = """maestro.py task create \
  -v {PATH} \
  -t user.jodafons.data17_13TeV.AllPeriods.sgn.probes_lhmedium_EGAM1.bkg.VProbes_EGAM7.GRL_v97.v11_et{ET}_eta{ETA}.r3 \
  -c user.jodafons.job_config.Zee_v11.10sorts.5inits \
  -d user.jodafons.data17_13TeV.AllPeriods.sgn.probes_lhmedium_EGAM1.bkg.VProbes_EGAM7.GRL_v97_et{ET}_eta{ETA}.npz \
  --sd "{REF}" \
  --exec "run_tuning.py -c %IN -d %DATA -r %REF -v %OUT -t v11 -b zee \
  --extraArgs '--type fusion --path_to_rings {RINGS} --path_to_shower {SHOWER}'" \
  --queue "gpu" """



for et in range(5):
    for eta in range(5):
        ref = "{'%%REF':'user.jodafons.data17_13TeV.AllPeriods.sgn.probes_lhmedium_EGAM1.bkg.VProbes_EGAM7.GRL_v97_et%d_eta%d.ref.pic.gz'}"%(et,eta)
        cmd = command.format(ET=et,ETA=eta,REF=ref, RINGS=path_to_rings.format(ET=et,ETA=eta), SHOWER=path_to_shower.format(ET=et,ETA=eta) )
        print(cmd)
        os.system(cmd)


