from spes import spes 

s = spes(7,B=0.99,eta=0.1,nrt=2,M=1e5,rh=3,project=True)


print " len r = ",len(s.r)



print " len mc = ",len(s.mc)
print " len phihat = ",len(s.dphidrhat1)

import pylab as plt

plt.ion()

plt.clf()

plt.plot(s.r, s.dphidrhat1)
plt.plot(s.r[s.nbound:], s.dphidrhat1[s.nbound:],lw=3)
