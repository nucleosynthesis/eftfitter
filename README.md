# eftfitter
Simple chi2 fits for H-EFT interpretation 

Based on [LHCHXSWG-INT-2017-01](https://cds.cern.ch/record/2290628/files/LHCHXSWG-INT-2017-001.pdf)

Requires workspace file `results.root` generated from [CombinedLimit](https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit) tool using EFT physics model.

You must run inside the `HiggsAnalysis/CombinedLimit` area inside `CMSSW` (to access model workspace)

   * Run with `python eftfitter.py`, which reads in the results from `HIG_18_029.py`.

   * Change EFT parameter choice by setting the variable `EFT_PARAMETERS = ["cG_x04","cHW_x02","cWWMinuscB_x03"]` inside `eftfitter.py`.

