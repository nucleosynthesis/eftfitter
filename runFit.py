from eftfitter import *

################### Import measurements ##############

import HIG_18_029_asimov as hgg_stxs 
import HIG_16_040        as hgg_s0
import HIG_19_001        as h4l_stxs
#import ATLAS36 as atlas

################# Pick set of parameters (POI set)

EFT_PARAMETERS = ["cGx16pi2_x04","cAx16pi2_x01","cu_x02","cHW_x02","cWWMinuscB_x03"] 
#EFT_PARAMETERS = ["cG_x04","cHW_x02","cWWMinuscB_x03"] 
fitter = eft_fitter(EFT_PARAMETERS)

############### CHOOSE YOUR DATA SETS TO INCLUDE, no correlations between them ##############
fitter.processModel(hgg_stxs,"hgg")
fitter.processModel(hgg_s0  ,"hgg")
fitter.processModel(h4l_stxs,"hzz")
#fitter.processModel(atlas,"hzz")
#############################################################################################
# import parameter config
import parameters_config_EFT as pconfig
fitter.prep(pconfig)
# Uncomment to set the other parameters in the model to their best fits in the fixed scans !
fitter.global_fit()
fitter.reset()  # < - Now the nominal is at the best fits!
##########################################################################################
for e in EFT_PARAMETERS: fitter.scan(e)

# 2D scans do not profile other POIs (yet) !!!!!
fitter.scan2d("cGx16pi2_x04","cHW_x02")
fitter.scan2d("cWWMinuscB_x03","cHW_x02")
fitter.scan2d("cWWMinuscB_x03","cGx16pi2_x04")
fitter.scan2d("cu_x02","cGx16pi2_x04")
fitter.scan2d("cAx16pi2_x01","cGx16pi2_x04")
fitter.scan2d("cAx16pi2_x01","cHW_x02")
fitter.scan2d("cAx16pi2_x01","cWWMinuscB_x03")
fitter.scan2d("cHW_x02","cu_x02")

