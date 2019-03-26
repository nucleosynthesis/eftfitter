import array
# last numbers are measured, symmetric error, leave as 1!
X = {
   'BRhggBRhzz' 		    : [[[1,'BR_hggBR_hzz']]			, 1.,0.690607734807 , 0.13812154696]
   ,'ggH_0J'                        : [[]					, 1.,1.07608695652 , 0.253623188406]
   ,'ggH_1J_low'              	    : [[[1,'ggH_1J_PTH_0_60']          ]	, 1.,0.666666666667 , 0.70454545454]
   ,'ggH_1J_med'	    	    : [[[1,'ggH_1J_PTH_60_120']	       ]	, 1.,1.0 , 0.565217391304          ]
   ,'ggH_1J_high'           	    : [[[1,'ggH_1J_PTH_120_200']       ]	, 1.,2.13333333333 , 1.33333333333 ]

   ,'ggH_2J_LT200_or_VBF' 	    : [[[1.26,'ggH_GE2J_PTH_0_60'],[2.0,'ggH_GE2J_PTH_60_120'],[1.0,'ggH_GE2J_PTH_120_200'],[0.38,'ggH_VBFTOPO_JET3' ],[0.27,'ggH_VBFTOPO_JET3VETO' ]]  , 1.,2.20833333333 , 0.916666666667]   
   ,'ggH_1J_BSM'             	    : [[ [0.16,'ggH_1J_PTH_GT200'],[0.23,'qqH_PTJET1_GT200']]					        						, 1.,2.34567901235 , 0.987654320988]
   ,'qqH_qq'			    : [[ [0.55,'qqH_VH2JET'],[2.86,'qqH_REST'],[0.91,'qqH_VBFTOPO_JET3VETO'],[0.34,'qqH_VBFTOPO_JET3']]					        	, 1.,1.78832116788 , 0.729927007299]   
   ,'VHLep'			    : [[ [16.2,'WH_lep_PTV_0_150'],[8.4,'ZH_lep_PTV_0_150'],[1.09,'WH_lep_PTV_150_250_0J'],[0.576,'ZH_lep_PTV_150_250_0J'],[0.86,'WH_lep_PTV_150_250_GE1J'],[0.40,'ZH_lep_PTV_150_250_GE1J'],[0.6,'WH_lep_PTV_GT250'],[0.33,'ZH_lep_PTV_GT250']]	, 1., 0.31746031746 , 1.26984126984 ]   
   ,'ttH'	  		    : [[[1,'ttH']]	, 1, 0.508474576271 , 0.762711864407]
} 

correlation = {
('BRhggBRhzz','BRhggBRhzz'):		1.
,('BRhggBRhzz','ggH_0J'):		-0.41
,('BRhggBRhzz','ttH'):			-0.07
,('BRhggBRhzz','VHLep'):		0.02
,('BRhggBRhzz','ggH_2J_LT200_or_VBF'):  -0.18
,('BRhggBRhzz','ggH_1J_med'):		-0.11
,('BRhggBRhzz','ggH_1J_low'):		0.06
,('BRhggBRhzz','ggH_1J_high'):		-0.23
,('BRhggBRhzz','ggH_1J_BSM'):		-0.4
,('BRhggBRhzz','qqH_qq'):		-0.48
,('ggH_0J','ggH_0J'):			1.0
,('ggH_0J','ttH'):			0.05
,('ggH_0J','VHLep'):			-0.04
,('ggH_0J','ggH_2J_LT200_or_VBF'):	0.04
,('ggH_0J','ggH_1J_med'):		0.09
,('ggH_0J','ggH_1J_low'):		-0.39
,('ggH_0J','ggH_1J_high'):		0.17
,('ggH_0J','ggH_1J_BSM'):		0.18
,('ggH_0J','qqH_qq'):			-0.1
,('ttH','ttH'):				1.0 
,('ttH','VHLep'):			-0.11
,('ttH','ggH_2J_LT200_or_VBF'):		-0.03
,('ttH','ggH_1J_med'):			0.03
,('ttH','ggH_1J_low'):			-0.02
,('ttH','ggH_1J_high'):			0.05
,('ttH','ggH_1J_BSM'):			-0.03
,('ttH','qqH_qq'):			0.05
,('VHLep','VHLep'):			1.0 
,('VHLep','ggH_2J_LT200_or_VBF'):	-0.02
,('VHLep','ggH_1J_med'):		-0.03
,('VHLep','ggH_1J_low'):		-0.01
,('VHLep','ggH_1J_high'):		-0.03
,('VHLep','ggH_1J_BSM'):		-0.03
,('VHLep','qqH_qq'):			0.
,('ggH_2J_LT200_or_VBF','ggH_2J_LT200_or_VBF'):	1.0
,('ggH_2J_LT200_or_VBF','ggH_1J_med'):	-0.13
,('ggH_2J_LT200_or_VBF','ggH_1J_low'):	0.02
,('ggH_2J_LT200_or_VBF','ggH_1J_high'):	-0.10
,('ggH_2J_LT200_or_VBF','ggH_1J_BSM'):	-0.03
,('ggH_2J_LT200_or_VBF','qqH_qq'):	-0.35
,('ggH_1J_med','ggH_1J_med'):		1.0 
,('ggH_1J_med','ggH_1J_low'):		-0.04
,('ggH_1J_med','ggH_1J_high'):		-0.12
,('ggH_1J_med','ggH_1J_BSM'):		0.10
,('ggH_1J_med','qqH_qq'):		-0.08
,('ggH_1J_low','ggH_1J_low'):		1.0
,('ggH_1J_low','ggH_1J_high'):		-0.05
,('ggH_1J_low','ggH_1J_BSM'):		0.01
,('ggH_1J_low','qqH_qq'):		-0.10
,('ggH_1J_high','ggH_1J_high'):		1.0
,('ggH_1J_high','ggH_1J_BSM'):		0.08
,('ggH_1J_high','qqH_qq'):		0.02
,('ggH_1J_BSM','ggH_1J_BSM'):		1.0
,('ggH_1J_BSM','qqH_qq'):		0.16
,('qqH_qq','qqH_qq'): 	1.
}
