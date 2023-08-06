from sample import sample

from limepy import limepy

M,rv,G=1,1,1
W0=5
k = limepy(W0,1,M=M,rv=rv,G=G,ode_rtoal=1e-8, ode_atol=1e-8)
s = sample(k, N=100, seed=123,verbose=True) # Check with discrete sample

