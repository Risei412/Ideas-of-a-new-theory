#!/usr/bin/env python3
import math
km, gh, Delta, omega = 0.6, 1.0, 0.0, 0.0
A=(km+gh)/2+1j*Delta
chi=1/(A-1j*omega)
t=1-km*chi
n0=0.5; r1,r2=0.6,-0.3; beta_prime=0.1
coef=km*gh*abs(chi)**2
n_out=coef*n0
alpha_prime=t*beta_prime
def ndot(th): return coef*(r1*math.cos(th)**2+r2*math.sin(th)**2)
def F(th):
    x=ndot(th)
    return 4*abs(alpha_prime)**2/(2*n_out+1)+x*x/(n_out*(n_out+1))
theta0=math.acos(math.sqrt(-r2/(r1-r2)))
print("fixed transfer =", t)
print("fixed baseline n_out =", n_out)
print("theta cancellation =", theta0)
print("F(theta=0) =", F(0))
print("F(theta_cancel) =", F(theta0))
print("ratio =", F(0)/F(theta0))
