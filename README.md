# eftfitter
Simple chi2 fits for H-EFT interpretation 

Based on [LHCHXSWG-INT-2017-01](https://cds.cern.ch/record/2290628/files/LHCHXSWG-INT-2017-001.pdf)

Requires workspace file `results.root` generated from [CombinedLimit](https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit) tool using EFT physics model (ask the author for a real one!).

You need to create a measurement file to (eg as in the `HIG_18_029.py` asimov data dummy example)

You must run inside the `HiggsAnalysis/CombinedLimit` area inside `CMSSW` (to access model workspace)

   * Run with `python eftfitter.py`, which reads in the results from `HIG_18_029.py`, `HIG_16_040.py` and `HIG-19-001.py`, which you need to get real inputs from the author (email if you are a member of the CMS collaboration and want to use them)

   * Change EFT parameter choice by setting the variable `EFT_PARAMETERS`, eg.  `EFT_PARAMETERS = ["cG_x04","cHW_x02","cWWMinuscB_x03"]` inside `eftfitter.py`.

The outputs will be 1D scans of the eft parameters (profiling the others or not) and some 2D scans, where the remaining parameters are fixed to 0.

