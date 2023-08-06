from sample import sample
from limepy import limepy
import pylab as plt
from pylab import sqrt
import numpy

k = limepy(7,1, G=1,M=1,rv=1)
rh = []
for i in range(20):
    s = sample(k, N=10000, seed=12345+i,verbose=False) # Check with discrete sample

    r = sqrt(s.x**2 + s.y**2 + s.z**2)
    m = numpy.loadtxt('m')

    asr = numpy.argsort(r)
    cm = numpy.cumsum(m[asr])
    M = cm[-1]
    rh.append( numpy.interp(0.5, cm/M, r[asr]))

    #print(" rh = ",rh[-1])
    print(" <rh> = ",rh[-1],numpy.median(rh), numpy.mean(rh), numpy.std(rh))
plt.ion()
plt.clf()

plt.scatter(r,m,s=0.1)
plt.loglog()
