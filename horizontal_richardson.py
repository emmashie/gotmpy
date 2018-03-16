import netCDF4 as nc
import numpy as np
from oceantools import seawater
from gotmpy import plotting_cmdruns
import matplotlib.pyplot as plt

def Rix(dsdx, h, uf, g=9.8, beta=7.7*10**-4):
    return g*beta*dsdx*h**2/uf**2
    

def friction_velocity(h, u, s, t, mu=0.00108):
    dudz = u[:,-1]-u[:,0]/h
    tau = mu*dudz
    rho = seawater.dens(s,t)
    return np.sqrt(tau/rho)
    
dat, u, v, zeta, salt, z = plotting_cmdruns.load_var("result.nc")
dsdz = plotting_cmdruns.calc_dsdz(salt,z)
h = np.squeeze(dat.variables["h"])
h = np.sum(h,axis=-1)
uf = friction_velocity(h, u, salt[:,-1], 20*np.ones(len(salt)))  
rix = Rix(-0.0001, h, 0.17*u[:,0])    
 
 
## plot parameter space
dsdx_min = 0
dsdx_max = 0.0003

h_min = 1
h_max = 30

uf_min = 0
uf_max = 0.2

n = 100 
dsdxr = np.linspace(dsdx_min, dsdx_max, n)
hr = np.linspace(h_min, h_max, n)
ufr = np.linspace(uf_min, uf_max, n)

# dsdx vs. uf
h = 15
dsdx, uf = np.meshgrid(dsdxr, ufr)

rix = Rix(dsdx, h, uf)

plt.figure(figsize=(10,6))
plt.pcolormesh(uf[1:,:], dsdx[1:,:], rix[1:,:], cmap="nipy_spectral")
plt.ylabel("ds/dx [psu/m]")
plt.xlabel("friction velocity [m/s]")
plt.colorbar()
plt.clim((0,100))
plt.xlim((0,0.1))
CS = plt.contour(uf[1:,:], dsdx[1:,:], rix[1:,:], levels=[0.1], colors='white')
fmt = {}
strs = ['threshold']
for l, s in zip(CS.levels, strs):
    fmt[l] = s
#loc = [(h_max*0.1,dbdx_max*0.5*1000), (h_max*0.2,dbdx_max*0.6*1000)]
plt.clabel(CS, CS.levels, inline=True, fmt=fmt, fontsize=10)

# vary u, const ds/dx, const h
u = np.linspace(0,1,25)
uf = 0.1*u
rix = Rix(0.0001, 15, uf)

