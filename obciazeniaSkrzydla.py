import matplotlib.pyplot as plt
import numpy as np
import math
import pandas as pd

# Read the CSV file into a DataFrame object
df = pd.read_csv('rozkladShrenka.csv')

# Convert the 'x' and 'y' columns to arrays
y = df['y [m]'].to_numpy()
Lmean = df['Jednostkowa sila nosna [N/m]'].to_numpy()

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
    else:
        c = variableValue[iVar]
    print(variableName[iVar], " = ", variableValue[iVar])

#Wiemy że 
L = MTOW

# Skrzydlo jest podzielone na 20 paskow
# dlugosc paska wynosi
yi = b/2/20
# Powierzchnia kadego paska wynosi
S_i = yi*c



# Srednia jednostkowa sila nosna na pasku
Lsr = np.zeros(20)
#Punkt zaczepienia wektora
ySil = np.zeros(20)

nrPasek = np.linspace(1, 20, 20)
nrPasek = nrPasek.astype(int)


for iPasek in range(0, 20):
    Lsr[iPasek] = np.mean([Lmean[iPasek], Lmean[iPasek+1]])
    #Punkt zaczepienia wektora
    ySil[iPasek] = y[iPasek] + yi/2

# Sila na paskach
LiPasek = np.ones(20)*Lsr*yi
fig = plt.figure(figsize=(8, 4))
plt.bar(nrPasek, LiPasek)
plt.xlabel('Kolejne segmenty')
plt.ylabel('L [N]')
plt.xticks(range(1,21), nrPasek)
plt.grid(True)
plt.savefig('L.png')
plt.show()
plt.close()

# Obcienia od skrzydla
mSkrzydla = 50 #kg
Wskrzydla = 50*9.81 #N
WnaPasek = np.ones(20)*Wskrzydla/20

fig = plt.figure(figsize=(8, 4))
plt.bar(nrPasek, WnaPasek, color='green')
plt.xlabel('Kolejne segmenty')
plt.ylabel('Ciezar skrzydla [N]')
plt.xticks(range(1,21), nrPasek)
plt.grid(True)
plt.savefig('W_skrzydla.png')
plt.show()
plt.close()

#Tu zebra wyniki i wyeksportowa do CSV!!!
# W exelu dodac sumy!!

# Sily tnace
T_L = np.zeros(21)
T_W = np.zeros(21)
Tsum = np.zeros(21)

for iPasek in range(19, -1, -1):
    T_L[iPasek] = T_L[iPasek+1]+LiPasek[iPasek]
    T_W[iPasek] = T_W[iPasek+1]-WnaPasek[iPasek]
    Tsum[iPasek] = Tsum[iPasek+1] + LiPasek[iPasek] - WnaPasek[iPasek]

fig = plt.figure(figsize=(8, 4))
plt.plot(y, T_L, '-o', color='green', markersize=3, label='Obciazenia aerodynamiczne')
plt.plot(y, T_W, '-o', color='red', markersize=3, label='Struktura skrzydla')
plt.plot(y, Tsum, '-o', color='magenta', markersize=3, label='Sumaryczne')
#plt.ylim(0, 10)
plt.xlabel('y [m]')
plt.ylabel('T [N]')
plt.grid(True)
plt.legend()
plt.savefig('T.png')
plt.show()
plt.close()

# Moment gnacy
Mg = np.zeros(21)
Mg[19] = 0 + yi/2*LiPasek[19]-WnaPasek[19]

for iPasek in range(19, -1, -1):
    Mg[iPasek] = Mg[iPasek+1] + yi/2*LiPasek[iPasek]-WnaPasek[iPasek]+Tsum[iPasek+1]*yi

fig = plt.figure(figsize=(8, 4))
plt.plot(y, Mg, '-o', color='magenta', markersize=3)
#plt.ylim(0, 10)
plt.xlabel('y [m]')

plt.ylabel('Mg [N*m]')
plt.grid(True)
plt.savefig('Mg.png')
plt.show()
plt.close()

#Moment skrecajacy
#Skos = 0
# Mamy profil symetryczny wiec Cm= 0
# Zatem moment skrecajacy 0
# Latwo
Ms = np.zeros(21)

# stack the vectors horizontally to create a table
table = np.column_stack((nrPasek, LiPasek, WnaPasek))

# export the table to a CSV file
np.savetxt('silyNaSkrzydle.csv', table, delimiter=',', header='Kolejne segmenty, Siła nośna [N], Ciężar skrzydła [N]', comments='', fmt='%f')

table2 = np.column_stack((y, T_L, T_W, Tsum, Mg, Ms))

# export the table to a CSV file
np.savetxt('silyWskrzydle.csv', table2, delimiter=',', header='y [m], T_L [N], T_W_skrzydła [N], Mg [N*m], Ms [N*m]', comments='', fmt='%f')