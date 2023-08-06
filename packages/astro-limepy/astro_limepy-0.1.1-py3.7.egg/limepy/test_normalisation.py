from __future__ import division
import scipy,numpy
from pylab import exp, sqrt, log10, pi
from scipy.special import erf, gamma, gammainc
from scipy.integrate import ode, dblquad
from math import factorial
from spes import spes
import matplotlib.pylab as plt
from matplotlib.pyplot import rc,axes

def get_df(v, r, s):
    df = s.df(r,v)
    return df

def integrate_DF(s):
    vmax = sqrt(2*s.phi[0])
    df, err = dblquad(lambda x, y: (4*pi*x*y)**2*get_df(x,y,s), 0, s.rt, lambda x: 0, lambda x: numpy.inf, epsabs=1e-8, epsrel=1e-8)
    return df, err


W0 = [7]
for i in range(len(W0)):
    s = spes(2,B=1e-4,eta=0.1)
    
    df, err =  integrate_DF(s)
    print(" Mj = %10.3e; Int df = %10.3e +/= %10.3e"%(s.M, df, err))

