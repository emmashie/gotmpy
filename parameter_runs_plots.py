import netCDF4 as nc
import numpy as np
import scipy
import matplotlib.pyplot as plt
plt.style.use('bmh')
plt.ion()
import re
import os
import gotmpy.plotting_cmdruns as cmd
plt.ioff()

basepath="/Users/emmashienuss/Google_Drive/1_Nutrient_Share/1_Projects_NUTRIENTS/Modeling/Scenario_Risk_Modeling/1D_Model_Tests/stratification_tests/1D_tests/"
dir = "dsdx_pgset"
outer = "%s%s/"%(basepath,dir)
os.chdir(outer)
dirs=[os.listdir(outer)[i] for i in range(len(os.listdir(outer)))  if os.path.isdir(os.listdir(outer)[i])]
N = len(dirs)

mld_dur = np.zeros(N)
outr = np.zeros(N)
umi = np.zeros(N)
uma = np.zeros(N)
os.chdir(outer)
for i in range(N):
    path = outer + dirs[i]
    os.chdir(path)
    file = path + "/" + "/result.nc"
    dat, u, v, zeta, salt, z = cmd.load_var(file)
    dsdz = cmd.calc_dsdz(salt,z)
    h = np.squeeze(dat["h"]) 
    time = np.squeeze(dat["time"])
    mld = cmd.calc_mld(salt,z)
    mld_dur[i] = cmd.calc_dur(mld,3)
    outr[i] = float(re.findall(r'-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *-?\ *[0-9]+)?',dirs[i])[0])
    xy = zip(outr.tolist(), mld_dur.tolist())
    xys = sorted(xy)
    x = np.asarray([xys[i][0] for i in range(len(xys))])
    y = np.asarray([xys[i][1] for i in range(len(xys))])
    umi[i] = np.min(np.mean(u,axis=-1))
    uma[i] = np.max(np.mean(u,axis=-1))
    if 1:
        fig, ax = plt.subplots(nrows=6,sharex=True, figsize=(6,9))
        ax[0].plot(u[:,-1])
        ax[0].set_title("u")
        ax[1].plot(np.mean(u,axis=-1))
        ax[1].set_title("ubar")
        ax[2].plot(zeta)
        ax[2].set_title("zeta")
        ax[3].plot(salt[:,-1])
        ax[3].set_title("surface salt")
        ax[4].plot(dsdz)
        ax[4].set_title("dsdz")
        ax[5].plot(mld)
        ax[5].set_title("mld")
        fig.savefig("%s/vars_timeseries.png"%(path))
        ax[0].set_xlim((0,60))
        fig.savefig("%s/vars_timeseries_zoom.png"%(path))
        plt.close("all")
    if 0:
        n = 24
        cmd.plot_profiles(salt[n:,:],z[n:,:])
        plt.title("salt profile hour:%s"%(str(n)))
        plt.savefig("%s/vars_prof24.png"%(path))
        n = 96
        cmd.plot_profiles(salt[n:,:],z[n:,:])
        plt.title("salt profile hour:%s"%(str(n)))
        plt.savefig("%s/vars_prof96.png"%(path))
        n = 204
        cmd.plot_profiles(salt[n:,:],z[n:,:])
        plt.title("salt profile hour:%s"%(str(n)))
        plt.savefig("%s/vars_prof204.png"%(path))
        plt.close("all")
    if 0:
        plt.figure()
        plt.plot(dsdz, zeta)
        plt.xlabel("ds/dz")
        plt.ylabel("water depth")
        plt.savefig("%s/dsdz_zeta_ss.png"%(path))
        plt.figure()
        n = 48
        plt.plot(dsdz[n:], zeta[n:])
        plt.xlabel("ds/dz")
        plt.ylabel("water depth")
        plt.savefig("%s/dsdz_zeta_ss48.png"%(path))
        plt.figure()
        n = 108
        plt.plot(dsdz[n:], zeta[n:])
        plt.xlabel("ds/dz")
        plt.ylabel("water depth")
        plt.savefig("%s/dsdz_zeta_ss108.png"%(path))
        plt.close("all")
    if 0:
        plt.figure(figsize=(9,5))
        plt.plot(dsdz)
        plt.ylabel("ds/dz")
        plt.xlabel("hours")
        plt.savefig("%s/dsdz.png"%(path))
        plt.close("all")
if 0: 
    plt.figure(figsize=(11,5))
    plt.plot(x,y, 'o-')
    plt.xlabel("tidal amp pg")
    plt.ylabel("duration of mixed layer less than 2 m [hours]")
    plt.savefig("%s/u_mld.png"%(outer))
    plt.close("all")    
if 0:
    xy0 = zip(outr.tolist(), umi.tolist())
    xys0 = sorted(xy0)
    x0 = np.asarray([xys0[i][0] for i in range(len(xys0))])
    y0 = np.asarray([xys0[i][1] for i in range(len(xys0))])
    xy1 = zip(outr.tolist(), uma.tolist())
    xys1 = sorted(xy1)
    x1 = np.asarray([xys1[i][0] for i in range(len(xys1))])
    y1 = np.asarray([xys1[i][1] for i in range(len(xys1))])
    plt.figure(figsize=(9,5))
    plt.plot(x,y0, 'o-')
    plt.plot(x,y1, 'o-')
    plt.ylabel("tidal velocity [m/s]")
    plt.xlabel("pressure gradient")
    plt.plot(outr, np.ones(len(outr))*0.4, 'k--', alpha=0.6)
    plt.plot(outr, np.ones(len(outr))*-0.4, 'k--', alpha=0.6)
    plt.savefig("%s/u_pg.png"%(outer))

