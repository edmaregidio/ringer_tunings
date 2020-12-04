import os


command = """maestro.py task create \
  -v $PWD \
  -t user.jodafons.data17_13TeV.AllPeriods.sgn.probes_lhmedium_EGAM2.bkg.VProbes_EGAM7.GRL_v97.v1_et{ET}_eta{ETA}.r1 \
  -c user.jodafons.job_config.Jpsiee_v1.n2to5.10sorts.5inits \
  -d user.jodafons.data17_13TeV.AllPeriods.sgn.probes_lhmedium_EGAM2.bkg.VProbes_EGAM7.GRL_v97_et{ET}_eta{ETA}.npz \
  --sd "{REF}" \
  --exec "run_tuning.py -c %IN -d %DATA -r %REF -v %OUT -t v1 -b jpsiee_fastcalo" \
  --queue "gpu" """



for et in range(3):
    for eta in range(5):
        ref = "{'%%REF':'user.jodafons.data17_13TeV.AllPeriods.sgn.probes_lhmedium_EGAM2.bkg.VProbes_EGAM7.GRL_v97_et%d_eta%d.ref.pic.gz'}"%(et,eta)
        cmd = command.format(ET=et,ETA=eta,REF=ref)
        print(cmd)
        os.system(cmd)


