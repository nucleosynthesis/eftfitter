from eftfitter import *

# import parameter config
import parameters_config_EFT as pconfig
#import parameters_config_kVkFkl as pconfig
################### Import measurements ##############

#import summer2019.HIG_18_029 as HIG_18_029 
#import summer2019.HIG_16_042 as HIG_16_042 
#import summer2019.HIG_18_018 as HIG_18_018 
#import summer2019.HIG_18_032 as HIG_18_032 
#import summer2019.HIG_16_044 as HIG_16_044 
#import summer2019.HIG_19_001 as HIG_19_001 
#import summer2019.HIG_17_035 as HIG_17_035 

import HIG_17_031.HIG_17_031  as comb2016
################# Pick set of parameters (POI set)

EFT_PARAMETERS = pconfig.MYPARAMS
fitter = eft_fitter(EFT_PARAMETERS)
fitter.doAsimov=True

############### CHOOSE YOUR DATA SETS TO INCLUDE, no correlations between them ##############
#fitter.processModel(HIG_18_029,"hgg")
#fitter.processModel(HIG_16_042,"hww")
#fitter.processModel(HIG_18_018,"hbb")
#fitter.processModel(HIG_19_001,"hzz")
#fitter.processModel(HIG_18_032,"htt")
#fitter.processModel(HIG_16_044,"hbb")
#fitter.processModel(HIG_17_035,"") # ttH with own decays

fitter.processModel(comb2016,"")
#############################################################################################
fitter.prep(pconfig)
# Uncomment to set the other parameters in the model to their best fits in the fixed scans !
#fitter.global_fit()
fitter.reset()  # < - Now the nominal is at the best fits!
##########################################################################################
for e in EFT_PARAMETERS: fitter.scan(e)

# 2D scans do not profile other POIs (yet) !!!!
for e in EFT_PARAMETERS: 
 for y in EFT_PARAMETERS: 
   if e == y: continue
   fitter.scan2d(e,y)
   fitter.scan2d(e,y,True)
