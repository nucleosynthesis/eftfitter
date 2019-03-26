ults.root` eftfitter
Simple chi2 fits for H-EFT interpretation 

Based on [LHCHXSWG-INT-2017-01](https://cds.cern.ch/record/2290628/files/LHCHXSWG-INT-2017-001.pdf)

Requires workspace file `results.root` generated from [CombinedLimit](https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit) tool using EFT physics model (ask the author for a real one!). 

You need to create a measurement file to (eg as in the `ATLAS36.py`  data  example) Note that the example here has a ratio of BRs which are "hardcoded" to be picked up by the fitter. If your model has special POIs which need to be created after the text2workspace.py step, then you must modify the code to handle it. 

You must run inside the `HiggsAnalysis/CombinedLimit` area inside `CMSSW` (to access model workspace)

   * Run with `python runFit.py`, which reads in the results from `ATLAS36.py` (for other modelswhich you need to get real inputs from the author (email if you are a member of the CMS collaboration and want to use them))

   * Change EFT parameter choice by setting the variable `EFT_PARAMETERS`, eg.  `EFT_PARAMETERS = ["cG_x04","cHW_x02","cWWMinuscB_x03"]` inside `runFit.py` -> all of the parameters, and ranges are defined in parameters_config_EFT.py, you can make a new config for other parameter sets 

The outputs will be 1D scans of the eft parameters (profiling the others or not) and some 2D scans, where the remaining parameters are fixed to 0.
Inside `runFit.py`, you can decide whether or not to run those scans or do a global fit first etc. 

If you want to fit another model (eg the kappa framework) you need to make a new `parameters_config.py` for it and set the names of the scaling functions prefix (`SCALING_FUNC_STR`) and input root file (`COMBINE_WS`) accordingly. 

