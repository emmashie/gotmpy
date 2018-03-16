#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt 
plt.ion()
plt.style.use('bmh')
import netCDF4 as nc 

def load_var(ncfile):
    dat = nc.Dataset(ncfile)
    u = np.squeeze(dat["u"])
    v = np.squeeze(dat["v"])
    zeta = np.squeeze(dat["zeta"])
    salt = np.squeeze(dat["salt"])
    z = np.squeeze(dat["z"])
    return dat, u, v, zeta, salt, z

def plot_profiles(var, z):
    plt.figure(figsize=(12,6))
    plt.plot(var[0,:], z[0,:], color='slategrey', label='low tide')
    plt.plot(var[1,:], z[1,:], color='dodgerblue', label='+1 hr')
    plt.plot(var[2,:], z[2,:], color='skyblue', label='+2 hrs')
    plt.plot(var[3,:], z[3,:], color='cadetblue', label='+3 hrs')
    plt.plot(var[4,:], z[4,:], color='c', label='+4 hrs')
    plt.plot(var[5,:], z[5,:], color='teal', label='+5 hrs')
    plt.plot(var[6,:], z[6,:], '--', color='darkslategrey', label='high tide')
    plt.plot(var[7,:], z[7,:], '--', color='teal', label='+7 hrs')
    plt.plot(var[8,:], z[8,:], '--', color='c', label='+8 hrs')
    plt.plot(var[9,:], z[9,:], '--', color='cadetblue', label='+9 hrs')
    plt.plot(var[10,:], z[10,:], '--', color='skyblue', label='+10 hrs')
    plt.plot(var[11,:], z[11,:], '--', color='dodgerblue', label='+11 hrs')
    plt.plot(var[12,:], z[12,:], '--', color='slategrey', label='low tide')
    plt.legend(loc='best', prop={'size':10})
    plt.xlabel("salinity $[ppt]$")
    plt.ylabel("depth $[m]$")

def plot_timeseries(title, u, v, zeta, salt, n, d):
    fig, ax = plt.subplots(nrows=4, sharex=True, figsize=(3,6))
    ax[0].set_title(title)
    ax[0].plot(u[n:n+d,-1])
    ax[0].set_ylabel("u velocity")
    ax[1].plot(v[n:n+d,-1])
    ax[1].set_ylabel("v velocity")
    ax[2].plot(zeta[n:n+d])
    ax[2].set_ylabel("zeta")
    ax[3].plot(salt[n:n+d,-1])
    ax[3].set_ylabel("salt")
    fig.tight_layout()
    
def calc_dsdz(salt,z):
    ds = salt[:,-1]-salt[:,0]
    dz = z[:,-1]-z[:,0]
    return ds/dz
    
def calc_mld(salt, z, threshold=0.01):
    # calculate ds/dz for each layer
    dsdz = np.zeros((len(salt[:,0]), len(z[0,:])-1))
    dsz = np.zeros((len(salt[:,0]), len(z[0,:])-1))
    for i in range(len(salt[:,0])):
        dsdz[i,:] = -np.diff(salt[i,:])/np.diff(z[i,:])[0]
        for j in range(len(z[0,:])-1):
            dsz[i,j] = np.mean([z[i,j],z[i,j+1]])
    # calculate mixed layer depth and strtification duration
    mld = np.zeros(len(salt[:,0]))
    for i in range(len(salt[:,0])):
        ind = np.argmax(dsdz[i,::-1]>threshold)
        if ind == 0:
            if dsdz[i,-1]<threshold:
                ind = 48 # all values are less than threshold so fully mixed 
            else:
                ind += 1
        mld[i] = dsz[i,len(dsdz[i,:]) - ind]
    return mld 

def calc_dur(mld, threshold):
    """ tstep in hours, default 1 hour
    """
    dur = 0
    durmax = 0
    for i in range(len(mld)):
        if np.abs(mld[i]) < threshold:
            dur+=1
        else:
            if dur>durmax:
                durmax=dur 
            dur=0
    return np.max([dur,durmax])




#dat, u, v, zeta, salt, z = load_var("result.nc")
