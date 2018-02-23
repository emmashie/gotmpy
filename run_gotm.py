#!/usr/bin/env python

import os
import numpy as np
import subprocess 

def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()
    
def set_dsdx(file_name="obs.nml", ln=269, value=-0.0001):
    dsdxtext = "   const_dsdx = %f,\n" % (value)
    replace_line(file_name, ln, dsdxtext)

def set_tauy(file_name="airsea.nml", ln=140, value=0.0025):
    tytext =  "   const_ty = %f,\n" % (value)
    replace_line(file_name, ln, tytext)
    
def set_mu(file_name="obs.nml", ln=221, value=0.5):
    mutext = "   AmpMu = %f,\n" % (value)
    replace_line(file_name, ln, mutext)
    
def set_h(file_name="gotmrun.nml", ln=48, value=15):
    htext = "   depth = %f,\n" % (value)
    replace_line(file_name, ln, htext)
    
temp_dir = "/Users/emmashienuss/Google_Drive/1_Nutrient_Share/1_Projects_NUTRIENTS/Modeling/Scenario_Risk_Modeling/1D_Model_Tests/stratification_tests/1D_tests/template_vel/"
results_base_dir = "/Users/emmashienuss/Google_Drive/1_Nutrient_Share/1_Projects_NUTRIENTS/Modeling/Scenario_Risk_Modeling/1D_Model_Tests/stratification_tests/1D_tests/"

### ds/dx only 
if 0: 
    dsdx_dir = results_base_dir + "dsdx_runs/"
    if not os.path.exists(dsdx_dir):
        os.makedirs(dsdx_dir)
    dsdx_min = 0 # psu/m
    dsdx_max = -0.0003 # psu/m
    n = 100
    dsdxr = np.linspace(dsdx_min, dsdx_max, n)
    for i in range(len(dsdxr)):
        run_name = "dsdx_%f" % (dsdxr[i])
        run_dir = dsdx_dir + run_name
        cmd = "cp -r %s %s" % (temp_dir, run_dir)
        subprocess.call(cmd,shell=True)
        obsfile = run_dir+"/obs.nml"
        ln = 269
        dsdxtext = "   const_dsdx = %f,\n" % (dsdxr[i])
        replace_line(obsfile, ln, dsdxtext)
        os.chdir(run_dir)
        subprocess.call("gotm",shell=True)
    
##### dsdx and windstress 
if 0: 
    # set up dsdx and windstress directories
    dsdxty_dir = results_base_dir + "dsdx_tauy_pg/"
    if not os.path.exists(dsdxty_dir):
        os.makedirs(dsdxty_dir)
    # set up dsdx range
    dsdx_min = 0 # psu/m
    dsdx_max = -0.0003 # psu/m
    n = 10
    dsdxr = np.linspace(dsdx_min, dsdx_max, n)
    # set up windstress range
    tauy_min = 0 # N/m^2
    tauy_max = 0.1 # N/m^2
    n = 10
    tauyr = np.linspace(tauy_min, tauy_max, n)
    # loop over dsdx 
    for i in range(len(dsdxr)):
        dsdx_name = "dsdx_%f" % (dsdxr[i])
        dsdx_dir = dsdxty_dir + dsdx_name 
        if not os.path.exists(dsdx_dir):
            os.makedirs(dsdx_dir)
        for j in range(len(tauyr)):
            tauy_name = "tauy_%f" % (tauyr[j])
            tauy_dir = dsdx_dir + "/" + tauy_name
            cmd = "cp -r %s %s" % (temp_dir, tauy_dir)
            subprocess.call(cmd,shell=True)
            obsfile = tauy_dir + "/obs.nml"
            set_dsdx(file_name=obsfile, value=dsdxr[i])
            airfile = tauy_dir + "/airsea.nml"
            set_tauy(file_name=airfile, value=tauyr[j])
            os.chdir(tauy_dir)
            subprocess.call("gotm",shell=True)
            

##### dsdx and tidal strength (mu)
if 0:
    # set up dsdx and tidal strength directories
    dsdxu_dir = results_base_dir + "dsdx_u_vel/"
    if not os.path.exists(dsdxu_dir):
        os.makedirs(dsdxu_dir)
    # set up dsdx range
    dsdx_min = 0 # psu/m
    dsdx_max = -0.0003 # psu/m
    n = 10
    dsdxr = np.linspace(dsdx_min, dsdx_max, n)
    # set up tidal range
    mu_min = 0
    mu_max = 1.0
    n = 10
    mur = np.linspace(mu_min, mu_max, n)
    # loop over dsdx
    for i in range(len(dsdxr)):
        dsdx_name = "dsdx_%f" % (dsdxr[i])
        dsdx_dir = dsdxu_dir + dsdx_name
        if not os.path.exists(dsdx_dir):
            os.makedirs(dsdx_dir)
        for j in range(len(mur)):
            mu_name = "mu_%f" % (mur[j])
            mu_dir = dsdx_dir + "/" + mu_name
            cmd = "cp -r %s %s" % (temp_dir, mu_dir)
            subprocess.call(cmd,shell=True)
            obsfile = mu_dir + "/obs.nml"
            set_dsdx(file_name=obsfile, value=dsdxr[i])
            set_mu(file_name=obsfile, value=mur[j])
            os.chdir(mu_dir)
            subprocess.call("gotm",shell=True)
            

##### dsdx and water depth 
if 0:
    # set up dsdx and water depth directories
    dsdxh_dir = results_base_dir + "dsdx_h_vel/"
    if not os.path.exists(dsdxh_dir):
        os.makedirs(dsdxh_dir)
    # set up dsdx range   
    dsdx_min = 0 # psu/m
    dsdx_max = -0.0003 # psu/m
    n = 10
    dsdxr = np.linspace(dsdx_min, dsdx_max, n)
    # set up water depth range
    h_min = 1
    h_max = 30
    n = 10
    hr = np.linspace(h_min, h_max, n)
    # loop over dsdx
    for i in range(len(dsdxr)):
        dsdx_name = "dsdx_%f" % (dsdxr[i])
        dsdx_dir = dsdxh_dir + dsdx_name
        if not os.path.exists(dsdx_dir):
            os.makedirs(dsdx_dir)
        for j in range(len(hr)):
            h_name = "h_%f" % (hr[j])
            h_dir = dsdx_dir + "/" + h_name
            cmd = "cp -r %s %s" % (temp_dir, h_dir)
            subprocess.call(cmd,shell=True)
            obsfile = h_dir + "/obs.nml"
            set_dsdx(file_name=obsfile, value=dsdxr[i])
            gotmfile = h_dir + "/gotmrun.nml"
            set_h(file_name=gotmfile, value=hr[j])
            os.chdir(h_dir)
            subprocess.call("gotm",shell=True)


##### water depth and tidal strength 
if 1:
    # set up water depth and tidal strength
    hmu_dir = results_base_dir + "h_mu_vel/"
    if not os.path.exists(hmu_dir):
        os.makedirs(hmu_dir)
    # set up water depth range
    h_min = 1
    h_max = 30
    n = 10
    hr = np.linspace(h_min, h_max, n)
    # set up tidal range
    mu_min = 0
    mu_max = 1.0
    n = 10
    mur = np.linspace(mu_min, mu_max, n)
    # loop over h 
    for i in range(len(hr)):
        h_name = "h_%f" % (hr[i])
        h_dir = hmu_dir + h_name
        if not os.path.exists(h_dir):
            os.makedirs(h_dir)
        for j in range(len(mur)):
            mu_name = "mu_%f" % (mur[j])
            mu_dir = h_dir + "/" + mu_name
            cmd = "cp -r %s %s" % (temp_dir, mu_dir)
            subprocess.call(cmd,shell=True)
            gotmfile = mu_dir + "/gotmrun.nml"
            set_h(file_name=gotmfile, value=hr[i])
            obsfile = mu_dir + "/obs.nml"
            set_mu(file_name=obsfile, value=mur[j])
            os.chdir(mu_dir)
            subprocess.call("gotm",shell=True)
