import matplotlib.pyplot as plt
import numpy as np
import math
import pandas as pd

#Wczytaj dane z poprzednich projektow
variableName, variableValue = np.loadtxt('daneSamolotu.txt', comments="#", skiprows=1, usecols=(0,1), unpack=True, delimiter='=', dtype = str)
variableValue = variableValue.astype(np.float64)

print("Data have been read:")
for iVar in range(0, len(variableName)):

    if variableName[iVar] == "S":
        S = variableValue[iVar]
    elif variableName[iVar] == "MTOW":
        MTOW = variableValue[iVar]
    elif variableName[iVar] == "b":
        b = variableValue[iVar]
    elif variableName[iVar] == "Vc":
        Vc = variableValue[iVar]
    else:
        c = variableValue[iVar]
    print(variableName[iVar], " = ", variableValue[iVar])

    #Pisze ze obwiednia w oparciu o CS-23

#Masa projektowa 
M = MTOW/10
a = 0.9/math.radians(9.3)#1/rad
#Getstosc powietrza
ro = 1.2255 #kg/m^2
CLmax = 1.325
CLmaxKl = 1.8
#Predkosc maksymalna
# Na razie zgodnie z CS-23 minimalny max to 125% predkosci przelotowej, zatem:
Vmax = Vc*1.25
print(Vmax)
#Predkosc minimalna
Vmin = (2*MTOW/ro/CLmax/S)**0.5

print(Vmin)
#Zrobi tabelke jak Justyna z M, g, S, b, V_H, V_S

#Wspolczynniki od obciazen manewrowych
n_max = 2+24000/(1984+10000)
n_min = -0.4*n_max

#Predkosci do obwiedni
Vs = (2*MTOW/ro/CLmax/S)**0.5
Vh = 1.2*Vs
Va = Vs*(n_max**0.5)
Vc = 2.4*(MTOW/S)**0.5
Vd = 1.25*Vc


#Wspolczynniki od podmochow
# Projektowe predkosci podmochow
Vb = Va #Zmieni na wykresie jesli wieksze!!

Uc = 15.24 #m/s
Ud = 7.62

mig = 2*(MTOW/S)/ro/c/a/9.81
kg = 0.88*mig/(5.3+mig)
Nuc = 1 + (kg*ro*Uc*a/2/(MTOW/S))*Vc
Nuf = 1 - (kg*ro*Uc*a/2/(MTOW/S))*Vc
Nud = 1 + (kg*ro*Ud*a/2/(MTOW/S))*Vd
Nue = 1 - (kg*ro*Ud*a/2/(MTOW/S))*Vd

Xa = np.linspace(0, Va, 100)
Xh = np.linspace(0, Va-21.9, 100)
Na = 0.5*ro*Xa**2*CLmax*S/MTOW
Nh = -0.5*ro*Xh**2*CLmax*S/MTOW
fig = plt.figure(figsize=(8, 6))
plt.plot(Xa, Na, color='magenta')
plt.plot(Xh, Nh, color='magenta')

Xad = np.array([Va, Vd])
Nad = np.array([n_max, n_max])
Xhf = np.array([Va-21.5, Vc])
Nhf = np.array([n_min, n_min])
plt.plot(Xad, Nad, color='magenta')
plt.plot(Xhf, Nhf, color='magenta')

Xdd = np.array([Vd, Vd])
Ndd = np.array([n_max, 0])
Xdf = np.array([Vc, Vd])
Ndf = np.array([n_min, 0])
plt.plot(Xdd, Ndd, color='magenta')
plt.plot(Xdf, Ndf, color='magenta')

#Podmuchy
XUc = np.array([0, Vc])
NUc = np.array([1, Nuc])
XUf = np.array([0, Vc])
NUf = np.array([1, Nuf])
XUd = np.array([0, Vd])
NUd = np.array([1, Nud])
XUe = np.array([0, Vd])
NUe = np.array([1, Nue])
plt.plot(XUc, NUc, '--', color='blue')
plt.plot(XUf, NUf, '--',color='blue')
plt.plot(XUd, NUd, '--', color='blue')
plt.plot(XUe, NUe, '--',color='blue')

XUcd = np.array([Vc, Vd])
NUcd = np.array([Nuc, Nud])
XUde = np.array([Vd, Vd])
NUde = np.array([Nud, Nue])
XUef = np.array([Vc, Vd])
NUef = np.array([Nuf, Nue])
plt.plot(XUcd, NUcd, color='blue')
plt.plot(XUde, NUde,color='blue')
plt.plot(XUef, NUef, color='blue')

#Linie laczace 
Vb = Va + 1.5
XUab = np.linspace(Va, Vb, 100)
NUab = 0.5*ro*XUab**2*CLmax*S/MTOW
plt.plot(XUab, NUab, color='blue')

XUbc = np.array([Vb, Vc])
NUbc = np.array([NUab[99], Nuc])
plt.plot(XUbc, NUbc, color='blue')

#Punkt h!
XUfh = np.array([Vh, Vc])
NUfh = np.array([-0.5*ro*Vh**2*CLmax*S/MTOW, Nuf])
plt.plot(XUfh, NUfh, color='blue')

#plt.ylim(0, 10)
plt.ylabel('N [-]')
plt.xlabel('V [m/s]')
plt.grid(True)
plt.savefig('obwiednia.png')
plt.show()
plt.close()
