#!/usr/bin/env python

import os
import numpy as np
from scipy.interpolate import interp1d
import subprocess 


def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    return array[idx]
        
def dsdx2dpdx(mu):
    g = 9.8
    h = 15
    beta = 0.000748
    dsdx = np.array([0.0, -0.000022, -0.000044, -0.000067, -0.000089, -0.000111, -0.000133, -0.000156, -0.000178, -0.000200])
    mu_thresh = np.array([2e-6, 4e-6, 6.6e-6])
    mu_ref = find_nearest(mu_thresh, mu)
    if mu_ref == 2e-6:
        alpha = np.array([0, 0.1, 0.099, 0.084, 0.078, 0.075, 0.075, 0.073, 0.07, 0.068])
    if mu_ref == 4e-6:
        alpha = np.array([0, 0.1, 0.099, 0.084, 0.078, 0.074, 0.070, 0.068, 0.066, 0.065])
    if mu_ref == 6.6e-6:
        alpha = np.array([0, 0.1, 0.099, 0.084, 0.078, 0.067, 0.064, 0.065, 0.062, 0.062])
    dpdx = -alpha*g*beta*(h/2)*dsdx
    return dsdx, dpdx

def lsg2pg(dsdx, mu):
    dsdxr, dpdxr = dsdx2dpdx(mu)
    f = interp1d(dsdxr,dpdxr,kind="cubic")
    return f(dsdx)

def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()
        
def set_param(param, value, base, filename=None, ln=None, text=None, mu=2e-6):
    if param=="dsdx":
        filename="%s/obs.nml"%(base)
        ln=269
        text = "   const_dsdx = %f,\n" % (value)
        replace_line(filename, ln, text)
        pg = lsg2pg(value, mu)
        ln = 217
        text = "   PressConstU = %.9f,\n" % (pg)
        replace_line(filename, ln, text)
    if param=="tauy":
        filename="%s/airsea.nml"%(base)
        ln=140
        text =  "   const_ty = %f,\n" % (value)
        replace_line(filename, ln, text)
    if param=="mu":
        filename="%s/obs.nml"%(base)
        ln=221
        text = "   AmpMu = %f,\n" % (value)
        replace_line(filename, ln, text)
    if param=="h":
        filename="%s/gotmrun.nml"%(base)
        ln=48
        text = "   depth = %f,\n" % (value)
        replace_line(filename, ln, text)
    if param=="bot_rough":
        filename="%s/gotmmean.nml"%(base)
        ln=76
        text = "   h0b = %f,\n" % (value)
        replace_line(filename, ln, text)
    if param=="pg":
        filename="%s/obs.nml"%(base)
        ln=217
        text = "   PressConstU = %f,\n" % (value)
        replace_line(filename, ln, text)
    if param=="velrel":
        filename="%s/obs.nml"%(base)
        ln=438
        text = "   vel_relax_tau = %f,\n" % (value)
        replace_line(filename, ln, text)
        
    
temp_dir = "/Users/emmashienuss/Google_Drive/1_Nutrient_Share/1_Projects_NUTRIENTS/Modeling/Scenario_Risk_Modeling/1D_Model_Tests/stratification_tests/1D_tests/template_pg/"
results_base_dir = "/Users/emmashienuss/Google_Drive/1_Nutrient_Share/1_Projects_NUTRIENTS/Modeling/Scenario_Risk_Modeling/1D_Model_Tests/stratification_tests/1D_tests/"

def run_param2D(basedir, tempdir, runname, oparam, iparam, omin, omax, imin, imax, n, mu=np.linspace(0,0.00002,10)):
    """ basedir: path to base directory to put GOTM runs in
        tempdir: path to location of template GOTM files
        runname: name of GOTM run, used at directory name for all run subdirectories
        oparam: parameter name for outer directory name base for GOTM runs
        iparam: parameter name for inner directory name base for GOTM runs
        omin: outer parameter minimum value
        omax: outer parameter maximum value
        imin: inner parameter minimum value
        imax: inner parameter maximum value
        n: number of runs for each parameter
    """
    rundir = basedir + runname + "/"
    if not os.path.exists(rundir):
        os.makedirs(rundir)
    # set up parameter ranges
    outr = np.linspace(omin, omax, n)
    inr = np.linspace(imin, imax, n)
    for i in range(len(outr)):
        outdir = rundir + "%s_%f"%(oparam,outr[i])
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        for j in range(len(inr)):
            indir = outdir + "/%s_%f"%(iparam,inr[j])
            cmd = "cp -r %s %s" % (tempdir, indir)
            subprocess.call(cmd,shell=True)
            if oparam == "dsdx":
                set_param(oparam, outr[i], indir,mu=mu[i])
            else:
                set_param(oparam, outr[i], indir)
            if iparam == "dsdx":
                set_param(iparam, inr[j], indir, mu=mu[j])
            else:
                set_param(iparam, inr[j], indir)
            os.chdir(indir)
            subprocess.call("gotm",shell=True)    


def run_param1D(basedir, tempdir, runname, param, min, max, n, mu=2e-6):
    """ basedir: path to base directory to put GOTM runs in
        tempdir: path to location of template GOTM files
        runname: name of GOTM run, used at directory name for all run subdirectories
        param: parameter name for directory name base for GOTM runs
        min: parameter minimum value
        max: parameter maximum value
        n: number of runs for each parameter
    """
    rundir = basedir + runname + "/"
    if not os.path.exists(rundir):
        os.makedirs(rundir)
    # set up parameter ranges
    pr = np.linspace(min, max, n)
    for i in range(len(pr)):
        dir = rundir + "%s_%f"%(param,pr[i])
        if not os.path.exists(dir):
            os.makedirs(dir)
        cmd = "cp -r %s %s" % (tempdir, dir)
        subprocess.call(cmd,shell=True)
        if param == "dsdx":
            set_param(param, pr[i], dir, mu=mu)
        else:
            set_param(param, pr[i], dir)
        os.chdir(dir)
        subprocess.call("gotm",shell=True) 


if 0: 
    runname = "dsdx_pgset"
    param = "dsdx"
    min = 0
    max = -0.0002
    n = 10
    #cmd = "cp -r %s %s/temp" % (temp_dir, results_base_dir)
    #subprocess.call(cmd,shell=True)
    set_param("mu", 0.000004, "%s/temp"%(results_base_dir))
    run_param1D(results_base_dir, results_base_dir + "/temp/", runname, param, min, max, n, mu=0.000004)


if 0: 
    runname = "bot_stress"
    oparam = "mu"
    omin = 0
    omax = 0.00001
    iparam = "bot_rough"
    imin = 5
    imax = 10
    n = 5
    run_param2D(results_base_dir, temp_dir, runname, oparam, iparam, omin, omax, imin, imax, n)



### ds/dx only 
if 0: 
    runname = "dsdx_runs"
    param = "dsdx"
    min = 0
    max = -0.0003
    n = 100
    run_param1D(results_base_dir, temp_dir, runname, param, min, max, n)
    


### u only 
if 0: 
    runname = "mu_runs_bs_075"
    param = "mu"
    min = 0
    max = 0.00002
    n = 25
    cmd = "cp -r %s %s/temp" % (temp_dir, results_base_dir)
    subprocess.call(cmd,shell=True)
    mnfile = results_base_dir + "/temp" + "/gotmmean.nml"
    set_param("bot_rough", 0.75, "%s/temp"%(results_base_dir))
    set_param("dsdx", -0.0001, "%s/temp"%(results_base_dir))
    run_param1D(results_base_dir, temp_dir, runname, param, min, max, n)


    
##### dsdx and windstress 
if 0: 
    runname = "dsdx_tauy_pg"
    oparam = "dsdx"
    omin = 0
    omax = -0.0003
    iparam = "tauy"
    imin = 0
    imax = 0.1
    n = 10
    run_param2D(results_base_dir, temp_dir, runname, oparam, iparam, omin, omax, imin, imax, n)
    
            

##### dsdx and tidal strength (mu)
if 1:
    runname = "dsdx_u_pg_new"
    oparam = "dsdx"
    omin = 0
    omax = -0.0003
    iparam = "mu"
    imin = 0
    imax = 0.00002
    n = 10
    run_param2D(results_base_dir, temp_dir, runname, oparam, iparam, omin, omax, imin, imax, n, mu=np.linspace(imin,imax,n))

            

##### dsdx and water depth 
if 0:
    runname = "dsdx_h_pg"
    oparam = "dsdx"
    omin = 0
    omax = -0.0003
    iparam = "h"
    imin = 1
    imax = 30
    n = 10
    run_param2D(results_base_dir, temp_dir, runname, oparam, iparam, omin, omax, imin, imax, n)
    


##### water depth and tidal strength 
if 0:
    runname = "h_mu_pg"
    oparam = "h"
    omin = 1
    omax = 30
    iparam = "mu"
    imin = 0
    imax = -0.00001
    n = 10
    run_param2D(results_base_dir, temp_dir, runname, oparam, iparam, omin, omax, imin, imax, n)


