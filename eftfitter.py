#Simply python fitting for STXS->EFT interpretation : 
from scipy.optimize import minimize
from scipy import linalg 
import array,numpy,sys

import matplotlib
matplotlib.use('Agg')

from matplotlib import pyplot as plt
import matplotlib.cm as cm 

import ROOT as r 

VERB=False
NSCANPOINTS=60

class eft_fitter:
  def __init__(self, EFT_PARAMETERS):   # for now lets just play, user interface later
    
    self.EFT_PARAMETERS = EFT_PARAMETERS 
  
    self.MODELS = []
    self.functions = {}
    self.doAsimov=False

  def processModel(self,model,decay):

   # make weights sum to 1
   for x in model.X.items():
    names = x[1][0] 
    if len(names) == 0: 
       x[1][0] = names = [[1.,x[0]]]
    elif len(names) == 0: 
       x[1][0][0] = 1. 
    else: 
     tsc=0
     for name in names: 
	  weight = float(name[0])
	  tsc+=weight
     for i in range(len(names)): 
	  x[1][0][i][0] /= tsc # renormalise


   # covert the correlation dict into a matrix 
   ccorr = []
   #print "correlation", model.correlation
   for x in model.X.items():
    for y in model.X.items(): 
      if (x[0],y[0]) in model.correlation.keys() :
         rho = model.correlation[(x[0],y[0])]
      elif (y[0],x[0]) in model.correlation.keys() : rho = model.correlation[(y[0],x[0])] 
      #print x[0],y[0],rho 
      else: 
        if x[0]==y[0]: rho=1.
        else: rho = 0. 
        print "WARNING - Assuming correlation in %s (no info given) rho(%s,%s) = %g"%(model,x[0],y[0],rho)
      ccorr.append(rho)

   model.correlation = array.array('d',ccorr)
   model.decay = decay 

   # symmetrize the errors 
   error_vector = []  
   for x in model.X.items(): error_vector.append(x[1][3])

   # do some squarification and inverting 
   model.nbins = len(model.X.items())
   v = model.correlation
   model.square_correlation = [v[i:i+model.nbins] for i in xrange(0,len(v),model.nbins)]
   model.variance = error_vector
   model.square_covariance = [ [ model.square_correlation[i][j] * (model.variance[i]*model.variance[j])\
				    for i in xrange(model.nbins)]\
				    for j in xrange(model.nbins)]

   model.err_mat = numpy.array(model.square_covariance)
   model.err_mat = linalg.inv(model.err_mat)

   # finally - if we want an Asimov, just set the observed number to the SM one 
   if  self.doAsimov :
    for x in model.X.items(): 
      x[1][2]=x[1][1]

   self.MODELS.append(model)


  def print_EFT(self):
    print " ---- EFT Parameter Values ---- " 
    for eft in self.EFT.items():
      print "%s = %g"%(eft[0],eft[1][1])
    print " ------------------------------ " 

  def print_X(self):
    print " ---- STXS Parameter Values ---- " 
    for i,M in enumerate(self.MODELS): 
      X = M.X
      print "Data set %d"%i
      for x in X.items():
       print "%s = %g +/- %g (measured), %g (predicted at EFT values) "%(x[0]+"_"+M.decay,x[1][2],x[1][3],x[1][1])
    print " ------------------------------ " 

  def get_x0(self,MINDEX):
   
    X = self.MODELS[MINDEX].X
    return [x[1][2] for x in X.items()]

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
  
  def get_x(self,vals,MINDEX,include_names=False):

    # This function should really not define how the scaling is done -> Project for MSci to generalise
    #if VERB: print " Setting following (to recalculate STXS bins) --> " , vals
    for v in vals:
      self.EFT[v[0]][1] = v[1]
      self.w.var(v[0]).setVal(v[1])      

    # note that some models may use a different naming for the SCALING function string (eg stage1 vs 1.1)
    model = self.MODELS[MINDEX] 
    old_scalefunctionstr = self.scalefunctionstr
    try: 
     self.scalefunctionstr = model.scalefunctionstr
    except: 
     pass 

    emptySet = r.RooArgSet()
    for x in model.X.items():
      names = x[1][0] 
      if not len(names) : 
      	names = [[1.,x[0]]]
      tsc = 0.
      #print "New list -> ", x[0],names 
      for name in names: 
        weight = float(name[0])
	name = name[1]
	#sc = model.getScalingForProcess() <- would be nice to use the .txt files instead of the ROOT object?
	if "R_BR" in name: # in this case, we have a ratio of ratios model, expect parameter BR_hxx_BR_hyy - THIS IS VERY SPECIFIC TO SOME MODELS (eg STXS combination)! 
	  Bxx = name.split("BR_")[1] 
	  Byy = name.split("BR_")[2]
	  #print "BR scaling ->", "%s_BR_%s"%(self.scalefunctionstr,Bxx)
	  #print "BR scaling ->", "%s_BR_%s"%(self.scalefunctionstr,Byy)
	  nom  = self.w.function("%s_BR_%s"%(self.scalefunctionstr,Bxx)).getVal(r.RooArgSet())
	  dnom = self.w.function("%s_BR_%s"%(self.scalefunctionstr,Byy)).getVal(r.RooArgSet())
	  sc = nom/dnom
	#else: sc = self.w.function("%s_%s_%s_13TeV"%(self.scalefunctionstr,name,model.decay)).getVal(r.RooArgSet())
	else:
	  if len(model.decay): scaling_str = "%s_%s_%s_13TeV"%(self.scalefunctionstr,name,model.decay)
	  else: scaling_str = "%s_%s_13TeV"%(self.scalefunctionstr,name)

	  # 1 - Look in the existing functions for it 
	  if scaling_str not in self.functions.keys(): 
	   if (self.w.function(scaling_str)!=None):
	     self.functions[scaling_str] = self.w.function(scaling_str)
	   else: 
	     # Look for the splitting of prod * dec and make a new function 
	     print "Will need to make the scaler for ", name.split("_")
	     prod_name  = "%s_%s"%(self.scalefunctionstr,"_".join(name.split("_")[0:-1]))
	     decay_name = "%s_BR_%s"%(self.scalefunctionstr,name.split("_")[-1])
	     print " Production name = ", prod_name 
	     print " Decay name = ", decay_name
	     if (self.w.function(prod_name)==None):  sys.exit("Error - couldn't find any way to make scaling function for %s_%s"%(name,model.decay))
	     if (self.w.function(decay_name)==None): sys.exit("Error - couldn't find any way to make scaling function for %s_%s"%(name,model.decay))
	     print "Creating scaling process %s in model %s --> "%(name,model), scaling_str
	     self.w.factory("prod::%s(%s,%s)"%(scaling_str,prod_name,decay_name))
	     self.functions[scaling_str] = self.w.function(scaling_str)
	  #print "Looking for function -> ",scaling_str
          sc = self.functions[scaling_str].getVal(emptySet)

	#sc = self.w.function("%s_%s_%s_13TeV"%(self.scalefunctionstr,name,model.decay)).getVal(r.RooArgSet())  #-> Back to here for EFT part!
	#sc = self.w.function("%s_%s_13TeV"%(self.scalefunctionstr,name)).getVal(r.RooArgSet())	
	#print " at params ", vals , " ....... " 
	#print " function ", scaling_str, " = ", sc
	tsc+=weight*sc 
      model.X[x[0]][1]=tsc   
    self.scalefunctionstr = old_scalefunctionstr
    if include_names: return [(x[0]+"_"+model.decay,x[1][1]) for x in model.X.items()]
    else : return [x[1][1] for x in model.X.items()]
  
  def get_dx(self): 
    return 0 # currently not implemented but would be good to include derivative part (nice project for MSCi students) 

  def calculate_x(self,vals): 
    #if VERB: print " Setting following (to recalculate STXS bins) --> " , vals
    for i in xrange(len(self.MODELS)): self.get_x(vals,i)
    #if VERB:
    # self.print_EFT()
    # self.print_X()

  def neg_log_likelihood(self,ECFG,*args):
    #print " my current EFT ", E
    args= args[0]
    #print ECFG
    E = [ [i,e] for i,e in zip(args['eft_keys'],ECFG)]

    constr=0
    for i, M in enumerate(self.MODELS):
      x  = self.get_x(E,i)
      x0 = self.get_x0(i)

      xarr  = numpy.array([xx-xx0 for xx,xx0 in zip(x,x0)])
      xarrT = xarr.T

      constr += 0.5*(xarrT.dot(M.err_mat.dot(xarr)))
    
    return constr
 
  def minimizer(self,rv={},constrained=False,params_list=[]):  # params_list is now list of POI

   #print "Asking for minimizer constrained ==", constrained
   #print "at fixed point ", rv
   #print "for params", params_list
   if constrained:
     for i in range(len(params_list)):
       self.EFT[params_list[i]][1]=rv[params_list[i]] 
     E=[[e[0],float(e[1][1])] for e in self.EFT.items()]
     self.calculate_x(E)

   self.EFT_safe = self.EFT.copy()

   #if constrained and params_list: 
   self.EFT = dict(E for E in filter(lambda x: x[0] not in params_list, self.EFT.items()))

   init_CFG = [[e[0],float(e[1][1])] for e in self.EFT.items()]
   eft_keys = {"eft_keys":[i[0] for i in init_CFG]}
   init = [i[1] for i in init_CFG]

   if VERB: print "My EFT parameter list is --> ", params_list
   results = []
   if params_list: 
      results = [ [params_list[i],rv[params_list[i]]] for i in range(len(params_list)) ]

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

  def prep(self,config):
    # 1. Set all the things to 0 
    #print self.calculate_x([0 for i in self.EFT.items()])
    # 2. remove the useless parameters from the list (user asks for only some of them anyway)
    self.EFT = config.PARAMS
    fw = r.TFile.Open(config.COMBINE_WS)
    self.w = fw.Get("w")     
    
    self.scalefunctionstr = config.SCALING_FUNC_STR

    fi = r.TFile("inputs_converted.root","RECREATE")
    for i,M in enumerate(self.MODELS): 
     d = fi.mkdir("DataSet_%d"%i)
     # make a weird ROOT file of the results why not ?
     hcorr = r.TH2F("h2corr","Correlations",M.nbins,0,M.nbins,M.nbins,0,M.nbins)
     hcov  = r.TH2F("h2cov","Covariance",M.nbins,0,M.nbins,M.nbins,0,M.nbins)
     hgr   = r.TH1F("hgr","Fitted values",M.nbins,0,M.nbins)
     hgr.SetMarkerStyle(20); hgr.SetMarkerSize(1.0); hgr.SetLineWidth(3)
     for i,x in enumerate(M.X.items()): 
      hgr.SetBinContent(i+1,x[1][2])
      hgr.SetBinError(i+1,M.variance[i])
      hgr.GetXaxis().SetBinLabel(i+1,x[0])
      hcorr.GetXaxis().SetBinLabel(i+1,x[0])
      hcov.GetXaxis().SetBinLabel(i+1,x[0])
      for j,y in enumerate(M.X.items()):
        hcorr.GetYaxis().SetBinLabel(j+1,y[0])
        hcorr.SetBinContent(i+1,j+1,M.square_correlation[i][j])
        hcov.GetYaxis().SetBinLabel(j+1,y[0])
        hcov.SetBinContent(i+1,j+1,M.square_covariance[i][j])
     hgr.GetYaxis().SetTitle("#mu #pm #sigma") 
     d.cd()
     hcorr.Write()
     hcov.Write()
     hgr.Write() 

    self.EFT = dict(E for E in filter(lambda x: x[0] in self.EFT_PARAMETERS, self.EFT.items()))

    for v in self.EFT.keys(): 
      xmin,xmax = self.EFT[v][0][0],self.EFT[v][0][1]
      #print "Config parameter ", v, self.w.var(v)
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
    for e in best_fit : self.EFT[e[0]][2]=e[1]
    self.print_EFT()

  def reset(self):
    # resets EFT parameters to 0 
    self.calculate_x([[e,self.EFT[e][2]] for e in self.EFT.keys()])

  def scan2d(self, px, py, profile=False): # set do_profile off here!
    # make a 2D scan of a likelihood 
    np = NSCANPOINTS 
    pxx = self.EFT[px]
    pyy = self.EFT[py]

    xx = numpy.linspace(pxx[0][0],pxx[0][1],np)
    yy = numpy.linspace(pyy[0][0],pyy[0][1],np)
    print " 2D scan in range " , px, " = ", pxx[0][0],"->",pxx[0][1], " x ", py, " = ", pyy[0][0], "->", pyy[0][1]
    C = []
    minll = 99999999
    for i in xrange(np):
      cc = []
      for j in xrange(np):

        self.reset()
	if profile: 
         res = self.minimizer(rv={px:xx[i],py:yy[j]},constrained=True,params_list=[px,py])
	#if res[1] < minll : minll = res[1]
        #C.append(res[1])
         nll2 =  res[1]
        else :
	 nll2 = 2*self.neg_log_likelihood([xx[i],yy[j]],{'eft_keys':[px,py]})

	if nll2<minll: minll = nll2
        cc.append(nll2)
	#print " -> ", xx[i],yy[j], nll2
      C.append(cc)
    C = numpy.array(C) 
    #print " ----> ? ", 0, 0, 2*self.neg_log_likelihood([0,0],{'eft_keys':[px,py]})
    # always start and end with a reset in any scan
    for c in xrange(len(C)): 
     for i in xrange(len(cc)): C[c][i] -= minll

    self.reset()

    a2D = plt.subplot(111)
    conts = plt.contour(yy,xx,C,levels=[2.3,5.99], colors='b')  # the way I constructed C, y, is the faster variable (think like a matrix)
    plt.clabel(conts, fontsize=9, inline=1)
    plt.contourf(yy,xx,C,levels=numpy.arange(0,6,0.2),cmap=cm.gray)  # the way I constructed C, y, is the faster variable (think like a matrix)
    cbar = plt.colorbar()
    a2D.set_ylabel(px)
    a2D.set_xlabel(py)
    cbar.ax.set_ylabel("$\Delta\chi^{2}$")
    a2D.axhline(0., linestyle='--', color='k') # horizontal lines
    a2D.axvline(0., linestyle='--', color='k') # vertical lines
    plt.ylim(pxx[0][0],pxx[0][1])
    plt.xlim(pyy[0][0],pyy[0][1])

    if profile: 
      plt.savefig("profile_2d_%s_%s.pdf"%(px,py));
      plt.savefig("profile_2d_%s_%s.png"%(px,py));
    else: 
      plt.savefig("scan_2d_%s_%s.pdf"%(px,py));
      plt.savefig("scan_2d_%s_%s.png"%(px,py));
    
    plt.clf()
    plt.cla()
    plt.close()
        
    
  
  def scan_LH(self,param, R,do_profile=True): 
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
    
    # in the scan, keep track of the scaling functions ... 
    scalers = []
    proc_scalers = []
    C = []
    minll = 9999
    for r in R : 
      if do_profile : 
        res = self.minimizer(rv={param:r},constrained=True,params_list=[param])
	if res[1] < minll : minll = res[1]
        C.append(res[1])
	scalers.append(res[0])
      else: 
        res = 2*self.neg_log_likelihood([r],{'eft_keys':[param]}) 
	if res< minll: minll = res
      	C.append(res)
      # now for every process, get the value of it 
      pscaler = []
      for MINDEX in range(len(self.MODELS)): 
        items = self.get_x([[param,r]],MINDEX,True)
	for item in items: pscaler.append(item)
      proc_scalers.append(pscaler)
      if VERB : 
        self.calculate_x([ [e[0],e[1][1]] for e in self.EFT.items() ])
	self.print_EFT()
        self.print_X()
    C = [c-minll for c in C]
    self.reset()
    return C,scalers,proc_scalers

  def scan(self,param): 
    

    """
      for x in self.X.items(): 
	scaler.append(x[1][2]) 
      scalers.append(scaler)
    """
    pv = self.EFT[param]
    np = NSCANPOINTS
    R = numpy.linspace(pv[0][0],pv[0][1],np)

    C_RES_PROF  = self.scan_LH(param,R,1)
    C_RES_FIXED = self.scan_LH(param,R,0)

    C_prof  = C_RES_PROF[0]
    C_fixed = C_RES_FIXED[0]

    profiled_POIs = C_RES_PROF[1]
    scaling_functions = C_RES_FIXED[2]
    
    fig, ax1 = plt.subplots()
    ax1.plot(R,C_prof,color='black',linewidth=3,linestyle='-',label="Profiled")
    ax1.plot(R,C_fixed,color='black',linewidth=3,linestyle='--',label="Scan")

    ax1.set_ylabel("$\Delta\chi^{2}$",fontsize=20)
    ax1.set_xlabel("%s"%param,fontsize=20)
    #plt.show()
    #if param in ["cG_x04","cHW_x02"]: 
    plt.ylim(0,10)
    
    if len(profiled_POIs[0]):
      ax2 = ax1.twinx()
      poilabels = []
      for P in [ p[0] for p in profiled_POIs[0] ]: poilabels.append(P)
      for i,P in enumerate(poilabels):
        vals = [p[i][1] for p in profiled_POIs]
        ax2.plot(R,vals, label=P)
        
        
      
      #for i,x in enumerate(self.X.items()): ax2.plot(R,[scalers[j][i] for j in range(len(R))], label=x[0])
      ax2.set_ylabel("Profiled EFT coeff.")
      ax2.legend(fontsize=9,loc='upper right')

    ax1.axvline(0., linestyle='--', color='k') 
    ax1.axhline(1., linestyle='--', color='r') # horizontal lines
    ax1.axhline(4., linestyle='--', color='r') # horizontal lines
    ax1.legend(fontsize=9,loc='upper left')
   
    plt.savefig("%s.pdf"%(param))
    plt.savefig("%s.png"%(param))
     
    plt.clf()
    plt.cla()
    plt.close()

    fig, ax1 = plt.subplots()
    styles = [".","v","+","o","*","s","x","p"]
    if len(scaling_functions): 
      scalers = []
      for P in [ p[0] for p in scaling_functions[0] ]: scalers.append(P)
      for i,P in enumerate(scalers):
        vals = [p[i][1] for p in scaling_functions]
        ax1.plot(R,vals,styles[i//7], label=P)

      ax1.set_ylabel("$\mu$",fontsize=20)
      ax1.set_xlabel("%s"%param,fontsize=20)
      box = ax1.get_position()
      ax1.set_position([box.x0*0.8, box.y0, box.width * 0.7, box.height])

      # Put a legend to the right of the current axis
      ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5),fontsize=6,ncol=2)
      plt.savefig("stxs_scaling_vs_%s.pdf"%(param))
      plt.savefig("stxs_scaling_vs_%s.png"%(param))
      
      plt.clf()
      plt.cla()
      plt.close()


