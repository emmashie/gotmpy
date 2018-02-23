import numpy as np
import matplotlib.pyplot as plt

dat = np.loadtxt("h_mu_vel.csv",delimiter=",")
dsdx = dat[1:,0]
tauy = dat[0,1:]
dmld = dat[1:,1:]

plt.figure()
plt.pcolormesh(tauy,dsdx,dmld/24,cmap="viridis")
plt.colorbar()
plt.xlabel("u [m/s]")
plt.ylabel("h [m]")
plt.title("u vs. ds/dx")

ddsdx = np.hstack([dsdx])
dtauy = np.hstack([tauy])
ddsdx, dtauy = np.meshgrid(ddsdx,dtauy)

def rbf(r,epsilon=0.5):
    return r*r*scipy.log(r)
    
good = np.isnan(dmld)==False
d1,d2 = np.meshgrid(ddsdx[good],ddsdx[good])
t1,t2 = np.meshgrid(dtauy[good],dtauy[good])
A = rbf(np.sqrt( (d1-d2)**2 + (t1-t2)**2))
A[np.isnan(A)] = 0.0
coefs = np.linalg.solve(A,dmld[good])






