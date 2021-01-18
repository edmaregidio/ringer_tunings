import os


# Path into the caloba cluster
path_to_rings = '~jodafons/tasks/user.jodafons.data17_13TeV.AllPeriods.sgn.probes_lhmedium_EGAM1.bkg.VProbes_EGAM7.GRL_v97.v9.rg_et{ET}_eta{ETA}.r1'
path_to_shower = '~jodafons/tasks/user.jodafons.data17_13TeV.AllPeriods.sgn.probes_lhmedium_EGAM1.bkg.VProbes_EGAM7.GRL_v97.v9.ss_et{ET}_eta{ETA}.r1'


command = """maestro.py task create \
  -v $PWD \
  -t user.jodafons.data17_13TeV.AllPeriods.sgn.probes_lhmedium_EGAM1.bkg.VProbes_EGAM7.GRL_v97.v9.et{ET}_eta{ETA}.r1 \
  -c user.jodafons.job_config.Zee_v9.rg.10sorts.2inits \
  -d user.jodafons.data17_13TeV.AllPeriods.sgn.probes_lhmedium_EGAM1.bkg.VProbes_EGAM7.GRL_v97_et{ET}_eta{ETA}.npz \
  --sd "{REF}" \
  --exec "run_tuning.py -c %IN -d %DATA -r %REF -v %OUT -t v9 -b zee_fastcalo \
  --extraArgs '--type fusion --path_to_rings {RINGS} --path_to_sjower {SHOWER}'" \
  --queue "gpu" """



for et in range(5):
    for eta in range(5):
        ref = "{'%%REF':'user.jodafons.data17_13TeV.AllPeriods.sgn.probes_lhmedium_EGAM1.bkg.VProbes_EGAM7.GRL_v97_et%d_eta%d.ref.pic.gz'}"%(et,eta)
        cmd = command.format(ET=et,ETA=eta,REF=ref, RINGS=path_to_rings.format(ET=et,ETA=eta), SHOWER=path_to_shower.format(ET=et,ETA=eta) )
        print(cmd)
        #os.system(cmd)


