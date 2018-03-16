import netCDF4 as nc
import numpy as np
import scipy
import matplotlib.pyplot as plt
plt.style.use('bmh')
plt.ion()
import re
import os
import gotmpy.plotting_cmdruns as cmd

basepath="/Users/emmashienuss/Google_Drive/1_Nutrient_Share/1_Projects_NUTRIENTS/Modeling/Scenario_Risk_Modeling/1D_Model_Tests/stratification_tests/1D_tests/"
dir = "dsdx_u_pg_zeta"
outer = "%s%s/"%(basepath,dir)
os.chdir(outer)
dirs=[os.listdir(outer)[i] for i in range(len(os.listdir(outer)))  if os.path.isdir(os.listdir(outer)[i])]
N = len(dirs)
inner = outer + dirs[0]
os.chdir(inner)
M = len([os.listdir(inner)[i] for i in range(len(os.listdir(inner))) if os.path.isdir(os.listdir(inner)[i])])

mld_dur = np.zeros((N,M))
outr = np.zeros((N,M))
inr = np.zeros((N,M))
os.chdir(outer)
for i in range(N):
    path = outer + dirs[i]
    os.chdir(path)
    sdirs = [os.listdir(".")[i] for i in range(len(os.listdir("."))) if os.path.isdir(os.listdir(".")[i])]
    for j in range(M):
        file = path + "/" + sdirs[j] + "/result.nc"
        dat = nc.Dataset(file)
        # load variables and get rid of extra dimensions
        salt = np.squeeze(dat["salt"])
        z = np.squeeze(dat["z"])
        h = np.squeeze(dat["h"]) 
        time = np.squeeze(dat["time"])
        mld = cmd.calc_mld(salt,z)
        mld_dur[i,j] = cmd.calc_dur(mld,2.5)
        outr[i,j] = float(re.findall(r'-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *-?\ *[0-9]+)?',dirs[i])[0])
        inr[i,j] = float(re.findall(r'-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *-?\ *[0-9]+)?',sdirs[i])[0])
        if 0:
            fig, ax = plt.subplots(nrows=6,sharex=True, figsize=(6,9))
            ax[0].plot(u[:,-1])
            ax[0].set_title("u")
            ax[1].plot(v[:,-1])
            ax[1].set_title("v")
            ax[2].plot(zeta)
            ax[2].set_title("zeta")
            ax[3].plot(salt[:,-1])
            ax[3].set_title("surface salt")
            ax[4].plot(dsdz)
            ax[4].set_title("dsdz")
            ax[5].plot(mld)
            ax[5].set_title("mld")
            ax[0].set_xlim()
            fig.savefig("%s/%s/vars_timeseries.png"%(path, sdirs[j]))
            plt.close("all")

f = open(outer+"%s.csv"%(dir),"w")
# write first row
f.write("0.00000,")
for i in range(len(inr[:,0])-1):
    f.write("%f," % (inr[i,0]))
f.write("%f" % (inr[-1,0]))
f.write("\n")
# loop through dsdx and mld 
for i in range(len(mld_dur[0,:])):
    f.write("%f," % (outr[i,0]))
    for j in range(len(mld_dur[:,0])-1):
        f.write("%f," % (mld_dur[i,j]))
    f.write("%f" % (mld_dur[i,-1]))
    f.write("\n")
f.close()
        



