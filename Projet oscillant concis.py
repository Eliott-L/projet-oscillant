from scipy.integrate import ode

import numpy as np

import matplotlib.pylab as plt


###############################################################################

### Variables

f0 = 10

w0 = 2.*np.pi*f0

Q0 = 6.

k0 = 20.

A0 = 1e-9

fs = 40. * f0

Tw = 120

Ts = 1./fs

N = int(Tw/Ts)

tab_f = np.linspace(0,2.*f0,N)

tab_t = np.linspace(0,Tw,N)
 
B=-10**19
 
###############################################################################

### Defintion des fonctions utilisees pour l'integration de l'eq. diff et cacluls des osccilations

def Force(t,z,Aexc,fexc,B, sens='croissant'): # Fonction de la force totale agissant sur l'oscillateur qui peut dependre de plusieurs parametres

    if sens == 'croissant':
        Fexc = k0*Aexc*np.cos(2.*np.pi*fexc*t) # force d'excitation harmonique
        
    if sens == 'decroissant':
        Fexc = k0*Aexc*np.cos(2.*np.pi*fexc*(Tw-t))
        
    Fnl = B*z**3 # force d'excitation non lineaire
    
    F_tot = Fexc + Fnl
    
    return F_tot
    
    

def E(t,z,zp,Aexc,fexc,B, sens='croissant'): # Fonction E de RK4 qui peut dependre de plusieurs parametres
    return ((w0**2/k0)*Force(t,z,Aexc,fexc,B,sens)-(w0/Q0)*zp-w0**2*z)

 
 

def RK4(t,z,zp,Aexc,fexc,B, sens='croissant'):
    k1 = Ts*zp
    l1 = Ts*E(t,z,zp,Aexc,fexc,B,sens)
    
    k2 = Ts*(zp + l1/2)
    l2 = Ts*E(t + Ts/2, z+k1/2, zp + l1/2, Aexc, fexc,B,sens)
     
    k3 = Ts*(zp + l2/2)
    l3 = Ts*E(t+Ts/2, z+k2/2, zp+l2/2, Aexc ,fexc,B,sens)
    
    k4 = Ts*(zp + l3)
    l4 = Ts*E(t+Ts, z+k3, zp+l3, Aexc, fexc,B,sens)
    
    q1 = (k1+2*k2+2*k3+k4)/6
    q2 = (l1+2*l2+2*l3+l4)/6
    
    return([z+q1,zp+q2])


def Oscillations(Aexc,fexc,B, sens='croissant'):
    t = 0.
    z = 0.    
    zp= 1e-11
    tab_t = [t]
    tab_z = [z]
    tab_zp= [zp]
    if type(fexc)!=np.ndarray:
        for i in range(N-1):
            tab_z.append(RK4(t,tab_z[i],tab_zp[i], Aexc,fexc,B,sens)[0])
            tab_zp.append(RK4(t,tab_z[i],tab_zp[i], Aexc,fexc,B,sens)[1])
            t = t+Ts
            tab_t.append(t)
    else:
        for i in range(N-1):
            tab_z.append(RK4(t,tab_z[i],tab_zp[i], Aexc, fexc[i]/2,B,sens)[0])
            tab_zp.append(RK4(t,tab_z[i],tab_zp[i], Aexc, fexc[i]/2,B,sens)[1])
            t = t+Ts
            tab_t.append(t)
    return(tab_z,tab_zp)


def amp(B,f, sens='croissant'):
    z=Oscillations(A0/Q0,f,B,sens)[0]
    zp=Oscillations(A0/Q0,f,B,sens)[1]
    f_amp=[]
    amp=[]
    for i in range(len(zp)):
        if zp[i]*zp[i-1]<=0:
            amp.append(abs(z[i]))
            f_amp.append(f[i])
    return(amp,f_amp)
    
    
########## Plots



### Oscillations sans excitation

# z_1=Oscillations(0,0,0)[0] 
# z_exc = Oscillations(A0/Q0,f0,0)[0]
# 
# plt.figure()
# 
# plt.subplot(2,2,1)
# plt.plot(tab_t,z_1)
# plt.show()
# 
# plt.figure()
# plt.plot(tab_t[0:1000],z_1[0:1000])
# plt.show()
# 
# ## Oscillations à f0
# 
# 
# plt.figure()
# plt.plot(tab_t,z_exc)
# plt.show()
# 
# plt.figure()
# plt.plot(tab_t[0:1000],z_exc[0:1000])
# plt.show()


### Amplitude de 0 à 2*f0


# z_freq=Oscillations(A0/Q0,tab_f,0)[0]
# z_freq_nl = Oscillations(A0/Q0,tab_f,B)[0]
# 
# plt.figure()
# 
# plt.subplot(2,2,1)
# plt.plot(tab_f,z_freq)
# plt.title('Reponse impulsionnelle avec Beta=0')
# plt.grid()
# 
# plt.subplot(2,2,2)
# plt.plot(tab_f,z_freq_nl)
# plt.title('Reponse impulsionnelle B=-10e19')
# plt.grid()
# 
# plt.subplot(2,2,3)
# plt.plot(tab_f,Oscillations(A0/Q0,tab_f,-B)[0])
# plt.title('Reponse impulsionnelle B=10e19')
# plt.grid()
# 
# plt.subplot(2,2,4)
# plt.plot(amp(0,tab_f)[1],amp(0,tab_f)[0])
# plt.plot(amp(B,tab_f)[1],amp(B,tab_f)[0])
# plt.plot(amp(-B,tab_f)[1],amp(-B,tab_f)[0])
# plt.title('Amplitudes pour differentes oscillations')
# plt.grid()
# 
# plt.show()

f_down=np.linspace(2*f0,0,N)

plt.plot(amp(B,f_down,sens='decroissant')[1],amp(B,f_down,sens='decroissant')[0])
plt.plot(amp(B,tab_f)[1],amp(B,tab_f)[0])
plt.show()























