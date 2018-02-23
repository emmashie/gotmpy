import netCDF4 as nc 
import numpy as np 
from bisect import bisect
import matplotlib.pyplot as plt 
plt.style.use('bmh')
plt.ion()
import re
import os

# ds/dz for full water column
def calc_dsdz(salt,z):
    ds = salt[:,-1]-salt[:,0]
    dz = z[:,-1]-z[:,0]
    return ds/dz

outer = "/Users/emmashienuss/Google_Drive/1_Nutrient_Share/1_Projects_NUTRIENTS/Modeling/Scenario_Risk_Modeling/1D_Model_Tests/stratification_tests/1D_tests/dsdx_tauy_vel/"
os.chdir(outer)
dirs=[os.listdir(outer)[i] for i in range(len(os.listdir(outer)))  if os.path.isdir(os.listdir(outer)[i])]
N = len(dirs)
inner = outer + dirs[0]
os.chdir(inner)
M = len([os.listdir(inner)[i] for i in range(len(os.listdir(inner))) if os.path.isdir(os.listdir(inner)[i])])

minmld = np.zeros((N,M))
maxmld = np.zeros((N,M))
avgmld = np.zeros((N,M))
mindsdz = np.zeros((N,M))
maxdsdz = np.zeros((N,M))
avgdsdz = np.zeros((N,M))
dsdx = np.zeros((N,M))
tauy = np.zeros((N,M))
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
        full_dsdz = calc_dsdz(salt,z)
        # calculate ds/dz for each layer
        dsdz = np.zeros((len(time), len(z[0,:])-1))
        dsz = np.zeros((len(time), len(z[0,:])-1))
        for t in range(len(time)):
            #dsdz[i,:] = (salt[i,:-1]-salt[0,1:])/h[i,0] # h (thickness) doesn't vary with depth
            dsdz[t,:] = -np.diff(salt[i,:])/h[i,0]
            for s in range(len(z[0,:])-1):
                dsz[t,s] = -np.sum(h[t,s:])+h[t,0]/2 # calculate depths from layer thickeness assume bottom layer is sum of all thickness, set stratification depth as halfway between layers
        # calculate mixed layer depth and strtification duration
        threshold = 0.003
        #threshold = 0.01
        mld = np.zeros(len(time))
        for t in range(len(time)):
            #ind = bisect(dsdz[i,::-1],threshold)  # finds first value greater than threshold 
            #ind = [n for n,l in enumerate(dsdz[i,::-1]) if l>threshold][0]
            ind = np.argmax(dsdz[t,::-1]>threshold)
            if ind == 0:
                if dsdz[t,-1]<threshold:
                    ind = 48 # all values are less than threshold so fully mixed 
                else:
                    ind += 1
            mld[t] = dsz[t,len(dsdz[t,:]) - ind]
            #mld[i] = dsz[i,ind] 
        print(dirs[i],sdirs[j],np.max(mld))         
        minmld[i,j] = np.min(mld)
        maxmld[i,j] = np.max(mld)
        avgmld[i,j] = np.mean(mld)
        mindsdz[i,j] = np.min(full_dsdz)
        maxdsdz[i,j] = np.max(full_dsdz)
        avgdsdz[i,j] = np.mean(full_dsdz)
        dsdx[i,j] = float(re.findall(r'-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *-?\ *[0-9]+)?',dirs[i])[0])
        tauy[i,j] = float(re.findall(r'-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *-?\ *[0-9]+)?',sdirs[i])[0])












