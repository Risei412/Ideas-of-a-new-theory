#!/usr/bin/env python3
# Reproducible W1 certificate. See adjacent JSON for frozen result.
import json, math, numpy as np
Omega=np.array([[0.35,0.18],[0.18,-0.42]],float)
Gm=np.diag([0.4,0.7]); Gh=np.diag([0.5,1.1])
Cm=np.diag(np.sqrt(np.diag(Gm))); sGh=np.diag(np.sqrt(np.diag(Gh)))
Nh=np.diag([0.15,3.0]); A=0.5*(Gm+Gh)+1j*Omega
def R(t): return np.array([[math.cos(t),-math.sin(t)],[math.sin(t),math.cos(t)]])
def Ch(t): return R(t)@sGh
def T(w): return np.eye(2)-Cm@np.linalg.inv(A-1j*w*np.eye(2))@Cm.T
def S(t,w):
    H=-Cm@np.linalg.inv(A-1j*w*np.eye(2))@Ch(t).conj().T
    return H@Nh@H.conj().T
def J(t,w=0.0):
    d=T(w)@np.array([1.,0.],complex); V=np.eye(2)+2*S(t,w)
    return float(4*np.real(d.conj().T@np.linalg.inv(V)@d))
ths=np.linspace(0,math.pi,721); vals=np.array([J(float(t)) for t in ths])
print("max ||Ch^†Ch-Gh|| =", max(np.linalg.norm(Ch(float(t)).conj().T@Ch(float(t))-Gh) for t in ths))
print("information range =", vals.min(), vals.max(), "ratio =", vals.max()/vals.min())
print("min Herm(A) eig =", np.min(np.linalg.eigvalsh((A+A.conj().T)/2)))
