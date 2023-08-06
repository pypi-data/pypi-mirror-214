from limepy import limepy
from numpy.random import randn

W0 = (3.82, 0.5*(0.8+1.05))
g = (1.77, 0.345)
F2 = (0.045, 0.5*(0.04+0.025))
f21 = (6.9, 0.5*(4.12+3.02))
ra = (5.97, 1.58)


W0_ = (W0[0] + 0*randn(1)*W0[1])[0]
g_ = (g[0] + 0*randn(1)*g[1])[0]
F2_ = (F2[0] + 0*randn(1)*F2[1])[0]
f21_ = (f21[0] + 0*randn(1)*f21[1])[0]
ra_ = (ra[0] + 0*randn(1)*ra[1] )[0]

#k = limepy(W0_, g_, delta=0.35,ra=ra_, Mj=[1-F2_, F2_], mj =[1, f21_], M=1, rv=1, G=1,meanmassdef='global', project=True,verbose=True)

k = limepy(W0_,g_, delta=0.35,ra=ra_,Mj=[8,2], mj=[1,3],M=1,rv=1,G=1,meanmassdef='global',verbosse=True,project=True)
print(k.rhj,k.rhpj)
