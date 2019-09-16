# Stage-0 Combination from CMS 2016 (36/fb) dataset - HIG-17-031 

# Best-fit values and (symmetrized) uncertainties from : http://cms-results.web.cern.ch/cms-results/public-results/publications/HIG-17-031/CMS-HIG-17-031_Table_005.pdf

# Interpret each XS as decay to ZZ --> will be scaled by BR(H->ZZ) as in measurement from CMS 

X = {
    'ggH_hzz'                        : [[], 1,1.00,0.175]
   ,'qqH_hzz'                        : [[], 1,0.66,0.290] 
   ,'VH_had_hzz'                     : [[[1,'WH_had_hzz']], 1,3.93,1.85]
   ,'WH_lep_hzz'                     : [[], 1,1.95,0.780]
   ,'ZH_lep_hzz'                     : [[], 1,0.84,0.500]             
   ,'ttH_hzz'                        : [[], 1,1.08,0.335]         
   ,'R_BR_hbbBR_hzz' 		    : [[], 1,0.96,0.375]
   ,'R_BR_httBR_hzz' 		    : [[], 1,0.98,0.315]
   ,'R_BR_hwwBR_hzz' 		    : [[], 1,1.30,0.265]
   ,'R_BR_hggBR_hzz' 		    : [[], 1,1.14,0.23]
#   'R_BR_hmmBR_hzz' 		    : [], 1,1,]
}

# Correlation values from: http://cms-results.web.cern.ch/cms-results/public-results/publications/HIG-17-031/CMS-HIG-17-031_Figure-aux_002.pdf
correlation = {
('ggH_hzz','ggH_hzz')         : 1.        
,('ggH_hzz','qqH_hzz')        : 0.13      
,('ggH_hzz','VH_had_hzz')     : -0.05 
,('ggH_hzz','WH_lep_hzz')     : 0.28
,('ggH_hzz','ZH_lep_hzz')     : 0.18
,('ggH_hzz','ttH_hzz')        : 0.38
,('ggH_hzz','R_BR_hbbBR_hzz'): -0.28 
,('ggH_hzz','R_BR_httBR_hzz'):-0.27
,('ggH_hzz','R_BR_hwwBR_hzz'):-0.73
,('ggH_hzz','R_BR_hggBR_hzz'):-0.67

,('qqH_hzz','qqH_hzz')        : 1. 
,('qqH_hzz','VH_had_hzz')     : 0.13 
,('qqH_hzz','WH_lep_hzz')     : 0.12
,('qqH_hzz','ZH_lep_hzz')     : 0.08
,('qqH_hzz','ttH_hzz')        : 0.17
,('qqH_hzz','R_BR_hbbBR_hzz'): -0.13 
,('qqH_hzz','R_BR_httBR_hzz'):-0.27
,('qqH_hzz','R_BR_hwwBR_hzz'):-0.26
,('qqH_hzz','R_BR_hggBR_hzz'):-0.30

,('VH_had_hzz','VH_had_hzz')     : 1. 
,('VH_had_hzz','WH_lep_hzz')     : 0.09
,('VH_had_hzz','ZH_lep_hzz')     : 0.06
,('VH_had_hzz','ttH_hzz')        : 0.11
,('VH_had_hzz','R_BR_hbbBR_hzz'): -0.09 
,('VH_had_hzz','R_BR_httBR_hzz'):-0.36
,('VH_had_hzz','R_BR_hwwBR_hzz'):-0.07
,('VH_had_hzz','R_BR_hggBR_hzz'):-0.32

,('WH_lep_hzz','WH_lep_hzz')     : 1.
,('WH_lep_hzz','ZH_lep_hzz')     : 0.24
,('WH_lep_hzz','ttH_hzz')        : 0.37
,('WH_lep_hzz','R_BR_hbbBR_hzz'): -0.63 
,('WH_lep_hzz','R_BR_httBR_hzz'):-0.18
,('WH_lep_hzz','R_BR_hwwBR_hzz'):-0.31
,('WH_lep_hzz','R_BR_hggBR_hzz'):-0.31

,('ZH_lep_hzz','ZH_lep_hzz')     : 1.
,('ZH_lep_hzz','ttH_hzz')        : 0.24
,('ZH_lep_hzz','R_BR_hbbBR_hzz'): -0.42 
,('ZH_lep_hzz','R_BR_httBR_hzz'):-0.13
,('ZH_lep_hzz','R_BR_hwwBR_hzz'):-0.20
,('ZH_lep_hzz','R_BR_hggBR_hzz'):-0.20

,('ttH_hzz','ttH_hzz')        : 1.
,('ttH_hzz','R_BR_hbbBR_hzz'): -0.52 
,('ttH_hzz','R_BR_httBR_hzz'):-0.32
,('ttH_hzz','R_BR_hwwBR_hzz'):-0.45
,('ttH_hzz','R_BR_hggBR_hzz'):-0.38

,('R_BR_hbbBR_hzz','R_BR_hbbBR_hzz'):1. 
,('R_BR_hbbBR_hzz','R_BR_httBR_hzz'):0.21
,('R_BR_hbbBR_hzz','R_BR_hwwBR_hzz'):0.33
,('R_BR_hbbBR_hzz','R_BR_hggBR_hzz'):0.31

,('R_BR_httBR_hzz','R_BR_httBR_hzz'):1.
,('R_BR_httBR_hzz','R_BR_hwwBR_hzz'):0.28
,('R_BR_httBR_hzz','R_BR_hggBR_hzz'):0.40

,('R_BR_hwwBR_hzz','R_BR_hwwBR_hzz'):1.0
,('R_BR_hwwBR_hzz','R_BR_hggBR_hzz'):0.58

,('R_BR_hggBR_hzz','R_BR_hggBR_hzz'):1.
}
