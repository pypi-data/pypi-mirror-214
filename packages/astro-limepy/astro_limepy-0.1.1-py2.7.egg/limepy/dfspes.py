from spes import spes
from pylab import exp
s = spes(7,B=0.1,eta=0.1)

print s.df(0,0)


phi = s.phi[0]

E = phi

print s.A[0]*(exp(E) - s.B - s.C*E)
