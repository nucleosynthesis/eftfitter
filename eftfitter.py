# Simply python fitting for STXS->EFT interpretation : 
from scipy.optimize import minimize
from scipy import linalg 
import array,numpy,sys
from matplotlib import pyplot as plt

import HIG_18_029 as model 

import ROOT as r 

VERB=False

class eft_fitter:
  def __init__(self, EFT_PARAMETERS):   # for now lets just play, user interface later
    
    self.EFT_PARAMETERS = EFT_PARAMETERS 

    fw = r.TFile.Open("result.root")    
    self.w = fw.Get("w")    
  
    self.X = model.X

    correlation = model.correlation 

    # symmetrize the errors 
    error_vector = model.error_vector


    self.EFT = {
    "clW_x02"           :[[-5 , 5    ]		,0]
    ,"cHu_x02"          :[[-1.1 , 1.1]		,0]
    ,"c2W"              :[[-5 , 5  	]	,0]
    ,"cl"               :[[-5 , 5  	]	,0]
    ,"cdG_x02"          :[[-5 , 5  	]	,0]
    ,"cH_x01"           :[[-1.4 , 1.94]		,0]
    ,"cpHL_x02"         :[[-5 , 5]		,0]
    ,"c2B"              :[[-5 , 5 ] 		,0]
    ,"cG_x04"           :[[-40. , 40.]		,0]
    ,"tcA_x04"          :[[-12 , 12 	]	,0]
    ,"cT_x03"           :[[-4.3 , 3.3 ] 	,0]
    ,"tc3W_x01"         :[[-1.8 , 1.8  ]	,0]
    ,"cWWPluscB_x03"    :[[-3.3 , 1.8  ]	,0]
    ,"cpHQ_x03"         :[[-4.4 , 4.4  ]	,0]
    ,"cHud_x02"         :[[-5 , 5  	]	,0]
    ,"cHe_x03"          :[[-1.8 , 0.25] 	,0]
    ,"cA_x04"           :[[-11 , 2.2 ]		,0]
    ,"cWWMinuscB_x03"   :[[-35 , 8  	]	,0]
    ,"tcHB_x01"         :[[-2.4 , 2.4]		,0]
    ,"cHQ_x03"          :[[-1.9 , 6.9 ] 	,0]
    ,"c3W_x02"          :[[-8.3 , 4.5  ]	,0]
    ,"cuB_x02"          :[[-5 , 5 	]	,0]
    ,"c2G_x04"          :[[-1.6 , 1.6 ] 	,0]
    ,"cu_x02"           :[[-8.4 , 15.5 ]	,0]
    ,"cHB_x02"          :[[-4.5 , 7.5  ]	,0]
    ,"c3G_x04"          :[[-1.6 , 1.6  ]	,0]
    ,"cdW_x02"          :[[-5 , 5  	]	,0]
    ,"cHW_x02"          :[[-3.5 , 10.5]		,0]
    ,"c6"               :[[-5 , 5  	]	,0]
    ,"tcHW_x02"         :[[-6 , 6  	]	,0]
    ,"tcG_x04"          :[[-1.2 , 1.2]		,0]
    ,"cHL_x02"          :[[-5 , 5  	]	,0]
    ,"cdB_x02"          :[[-5 , 5  	]	,0]
    ,"cuW_x02"          :[[-5 , 5  	]	,0]
    ,"cHd_x02"          :[[-4.2 , 0.44] 	,0]
    ,"cd_x02"           :[[-19.8 , 8.8 ]	,0]
    ,"clB_x02"          :[[-5 , 5  	]	,0]
    ,"cuG_x02"          :[[-5 , 5	]	,0]
    ,"tc3G_x04"         :[[-1.6 , 1.6]		,0]
    }
 

    # do some squarification and inverting 
    self.nbins = len(self.X.items())
    v = correlation
    self.square_correlation = [v[i:i+self.nbins] for i in range(0,len(v),self.nbins)]
    self.variance = error_vector
    self.square_covariance = [ [ self.square_correlation[i][j] * (self.variance[i]*self.variance[j])\
					  for i in range(self.nbins)]\
					  for j in range(self.nbins)]

    self.err_mat = numpy.array(self.square_covariance)
    self.err_mat = linalg.inv(self.err_mat)

    self.prep()


  def print_EFT(self):
    print " ---- EFT Parameter Values ---- " 
    for eft in self.EFT.items():
      print "%s = %g"%(eft[0],eft[1][1])
    print " ------------------------------ " 

  def print_X(self):
    print " ---- STXS Parameter Values ---- " 
    for x in self.X.items():
      print "%s = %g (measured), %g (predicted at EFT values) "%(x[0],x[1][1],x[1][2])
    print " ------------------------------ " 

  def get_x0(self):
    
    return [x[1][1] for x in self.X.items()]

  ############## Dummy Function to test Gaussian Constraint! #####################
  """
  def calculate_x(self,vals): 
    #print " I'm being asked to set the following " , vals
    for v in vals:
      self.EFT[v[0]][1] = v[1]
      self.w.var(v[0]).setVal(v[1])      

    for x in self.X.items():
      tsc=0.
      if x[0]=='ggH_0J': tsc=self.w.var('cG_x04').getVal()
      elif x[0]=='ggH_1J_low': tsc=self.w.var('cHW_x02').getVal()
      elif x[0]=='ggH_1J_med': tsc=self.w.var('cWWMinuscB_x03').getVal()
      self.X[x[0]][2]=tsc+1.
    return [x[1][2] for x in self.X.items()]
  """
  
  def calculate_x(self,vals): 
    if VERB: print " Setting following (to recalculate STXS bins) --> " , vals
    for v in vals:
      self.EFT[v[0]][1] = v[1]
      self.w.var(v[0]).setVal(v[1])      

    for x in self.X.items():
      names = x[1][0] 
      if not len(names) : 
      	names = [[1.,x[0]]]
      tsc = 0.
      #print "New list -> ", x[0],names 
      for name in names: 
        weight = float(name[0])
	name = name[1]
        sc = self.w.function("stxs1toeft_scaling_%s_hgg_13TeV"%name).getVal(r.RooArgSet())
	tsc+=weight*sc 
      self.X[x[0]][2]=tsc
    return [x[1][2] for x in self.X.items()]
  

  def neg_log_likelihood(self,ECFG,*args):
    #print " my current EFT ", E
    args= args[0]
    #print ECFG
    E = [ [i,e] for i,e in zip(args['eft_keys'],ECFG)]
    x  = self.calculate_x(E)
    x0 = self.get_x0()

    xarr  = numpy.array([xx-xx0 for xx,xx0 in zip(x,x0)])
    xarrT = xarr.T

    constr = 0.5*(xarrT.dot(self.err_mat.dot(xarr)))
    
    return constr
 
  def minimizer(self,rv=0,constrained=True,params_list=[]):  # params_list is now list of POI

   if constrained:
     self.EFT[params_list[0]][1]=rv
     E=[[e[0],float(e[1][1])] for e in self.EFT.items()]
     x  = self.calculate_x(E)

   self.EFT_safe = self.EFT.copy()

   #if constrained and params_list: 
   self.EFT = dict(E for E in filter(lambda x: x[0] not in params_list, self.EFT.items()))

   init_CFG = [[e[0],float(e[1][1])] for e in self.EFT.items()]
   eft_keys = {"eft_keys":[i[0] for i in init_CFG]}
   init = [i[1] for i in init_CFG]

   if VERB: print "My EFT parameter llist is --> ", params_list
   results = [params_list[0],rv]

   if len(init) :
        bounds = [(self.EFT[v][0][0],self.EFT[v][0][1]) for v in eft_keys['eft_keys']]
   	xbest = minimize(self.neg_log_likelihood,init,eft_keys,bounds=bounds)
	results = [[e[0],i] for e,i in zip(self.EFT.items(),xbest.x)]
   
   self.EFT = self.EFT_safe.copy()
   
   if VERB: 
     print "Finished a minimization ... " 
     print " ... Results = ", results
   
   self.calculate_x(results)
   
   if VERB: 
    self.print_EFT()
    self.print_X()

   return results, 2*self.neg_log_likelihood([r[1] for r in results],eft_keys)

  def prep(self):
    # 1. Set all the things to 0 
    #print self.calculate_x([0 for i in self.EFT.items()])
    # 2. remove the useless parameters from the list (user asks for only some of them anyway)

    # make a weird ROOT file of the results why not ?
    fi = r.TFile("inputs_converted.root","RECREATE")
    hcorr = r.TH2F("h2corr","Correlations",self.nbins,0,self.nbins,self.nbins,0,self.nbins)
    hgr   = r.TH1F("hgr","Fitted values",self.nbins,0,self.nbins)
    hgr.SetMarkerStyle(20); hgr.SetMarkerSize(1.0); hgr.SetLineWidth(3)
    for i,x in enumerate(self.X.items()): 
      hgr.SetBinContent(i+1,x[1][1])
      hgr.SetBinError(i+1,self.variance[i])
      hgr.GetXaxis().SetBinLabel(i+1,x[0])
      hcorr.GetXaxis().SetBinLabel(i+1,x[0])
      for j,y in enumerate(self.X.items()):
        hcorr.GetYaxis().SetBinLabel(j+1,y[0])
        hcorr.SetBinContent(i+1,j+1,self.square_correlation[i][j])
    fi.cd()
    hcorr.Write()
    hgr.Write() 

    self.EFT = dict(E for E in filter(lambda x: x[0] in self.EFT_PARAMETERS, self.EFT.items()))

    for v in self.EFT.keys(): 
      xmin,xmax = self.EFT[v][0][0],self.EFT[v][0][1]
      self.w.var(v).setMin(xmin)
      self.w.var(v).setMax(xmax)

    if VERB: 
     print "------- Setup state ------>"   
     self.print_X()
     self.print_EFT()
     print "-------------------------->"   

   
  def global_fit(self): 
    best_fit,nll2 = self.minimizer()
    self.calculate_x(best_fit)      # Note that this also sets the values of the EFT vector to the ones from the fit!
    self.print_EFT()

  def reset(self):
    # resets EFT parameters to 0 
    self.calculate_x([[e,0] for e in self.EFT.keys()])

  def scan2d(self, px, py): # set do_profile off here!
    # make a 2D scan of a likelihood, don't profile other things !    
    self.reset()
    np = 50 
    pxx = self.EFT[px]
    pyy = self.EFT[py]

    xx = numpy.linspace(pxx[0][0],pxx[0][1],np)
    yy = numpy.linspace(pyy[0][0],pyy[0][1],np)

    C = []
    for i in range(np):
      cc = []
      for j in range(np):
        nll2 = 2*self.neg_log_likelihood([xx[i],yy[j]],{'eft_keys':[px,py]})
        cc.append(nll2)
	#print " -> ", xx[i],yy[j], nll2
      C.append(cc)
    C = numpy.array(C) 
    #print " ----> ? ", 0, 0, 2*self.neg_log_likelihood([0,0],{'eft_keys':[px,py]})
    # always start and end with a reset in any scan
    self.reset()

    a2D = plt.subplot(111)
    plt.contourf(yy,xx,C,levels=numpy.arange(0,6,0.2))  # the way I constructed C, y, is the faster variable (think like a matrix)
    plt.colorbar()
    a2D.set_ylabel(px)
    a2D.set_xlabel(py)
    plt.savefig("scan_2d_%s_%s.pdf"%(px,py));
    plt.savefig("scan_2d_%s_%s.png"%(px,py));
    
    plt.clf()
    plt.cla()
    plt.close()
        
    
    
  def scan(self,param,do_profile=True): 
    
    # make a 1D scan of a particular EFT parameter, choose whether to profile remaining parameters or leave at 0 
    self.reset()
    if param not in self.EFT.keys() :
     print "No EFT parameter named: %s"%param
     exit()

    pv = self.EFT[param]
    print "Scanning %s in range [%g,%g]"%(param,pv[0][0],pv[0][1])

    #if not do_profile: params_list = self.EFT.keys()
    #else: params_list = [param]
    #if do_profile : print "List of profiled EFT params ? -> ", filter(lambda x: x not in params_list, self.EFT.keys())
    #else: print "Fixing all other EFT parameters in scan -> " ,filter(lambda x: x not in [param], self.EFT.keys())
    
    np = 40
    R = numpy.linspace(pv[0][0],pv[0][1],np)

    # in the scan, keep track of the scaling functions ... 
    scalers = []
    C = []
    for r in R : 
      scaler = []
      if do_profile : C.append(self.minimizer(rv=r,constrained=True,params_list=[param])[1])
      else: C.append(2*self.neg_log_likelihood([r],{'eft_keys':[param]}) )
      if VERB : self.print_X()
      for x in self.X.items(): 
	scaler.append(x[1][2]) 
      scalers.append(scaler)

    self.reset()

    fig, ax1 = plt.subplots()
    ax1.plot(R,C,color='black',linewidth=3,linestyle='--')
    ax1.set_ylabel("-2 Log(L)",fontsize=20)
    ax1.set_xlabel("%s"%param,fontsize=20)
    #plt.show()
    
    ax2 = ax1.twinx()
    for i,x in enumerate(self.X.items()): ax2.plot(R,[scalers[j][i] for j in range(len(R))], label=x[0])
    ax2.set_ylabel("bin scaling")

    ax2.legend(fontsize=9,loc=0)
    plt.savefig("%s_%g.pdf"%(param,do_profile))
    plt.savefig("%s_%g.png"%(param,do_profile))
     
    plt.clf()
    plt.cla()
    plt.close()

#EFT_PARAMETERS = ["cG_x04","cA_x04","cu_x02","cHW_x02","cWWMinuscB_x03"] 
EFT_PARAMETERS = ["cG_x04","cHW_x02","cWWMinuscB_x03"] 
fitter = eft_fitter(EFT_PARAMETERS)
#fitter.scan("cu_x02",0)
for e in EFT_PARAMETERS: fitter.scan(e,0)
for e in EFT_PARAMETERS: fitter.scan(e,1)
fitter.scan2d("cG_x04","cHW_x02")

