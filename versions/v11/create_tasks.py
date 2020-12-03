import os


# Path into the caloba cluster
path_to_v10 = '/home/jodafons/tunings/v10/user.jodafons.data17_13TeV.AllPeriods.sgn.probes_lhmedium_EGAM1.bkg.VProbes_EGAM7.GRL_v97.v10_et{ET}_eta{ETA}.r2/'
path_to_v9_ss = '/home/jodafons/tunings/v9_ss/user.jodafons.data17_13TeV.AllPeriods.sgn.probes_lhmedium_EGAM1.bkg.VProbes_EGAM7.GRL_v97.v9_ss_et{ET}_eta{ETA}.r0/'

command = """maestro.py task create \
  -v $PWD \
  -t user.jodafons.data17_13TeV.AllPeriods.sgn.probes_lhmedium_EGAM1.bkg.VProbes_EGAM7.GRL_v97.v11_et{ET}_eta{ETA}.r3 \
  -c user.jodafons.job_config.Zee_v11.10sorts.5inits \
  -d user.jodafons.data17_13TeV.AllPeriods.sgn.probes_lhmedium_EGAM1.bkg.VProbes_EGAM7.GRL_v97_et{ET}_eta{ETA}.npz \
  --sd "{REF}" \
  --exec "run_tuning.py -c %IN -d %DATA -r %REF -v %OUT -t v11 -b zee_fastcalo \
  --extraArgs '--type fusion --path_to_v10 {V10} --path_to_v9_ss {V9_SS}'" \
  --queue "gpu" """



for et in range(5):
    for eta in range(5):
        ref = "{'%%REF':'user.jodafons.data17_13TeV.AllPeriods.sgn.probes_lhmedium_EGAM1.bkg.VProbes_EGAM7.GRL_v97_et%d_eta%d.ref.pic.gz'}"%(et,eta)
        cmd = command.format(ET=et,ETA=eta,REF=ref, V10=path_to_v10.format(ET=et,ETA=eta), V9_SS=path_to_v9_ss.format(ET=et,ETA=eta) )
        print(cmd)
        os.system(cmd)


