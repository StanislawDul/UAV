import matplotlib.pyplot as plt
import numpy as np
import math
import pandas as pd

# Import data from txt
variableName, variableValue = np.loadtxt('daneSamolotu.txt', comments="#", skiprows=1, usecols=(0,1), unpack=True, delimiter='=', dtype = str)
variableValue = variableValue.astype(np.float64)

#Dispalay the input
print("Data have been read:")
for iVar in range(0, len(variableName)):

    if variableName[iVar] == "S":
        S = variableValue[iVar]
    elif variableName[iVar] == "MTOW":
        MTOW = variableValue[iVar]
    elif variableName[iVar] == "b":
        b = variableValue[iVar]
    elif variableName[iVar] == "c":
        c = variableValue[iVar]
    print(variableName[iVar], " = ", variableValue[iVar])

#Wiemy że 
L = MTOW
    
df = pd.read_csv('Mass_Table.csv', sep = ';')

#Elements = df['Element'].to_numpy()
#print(Elements)
#elemMasses = df['mass'].to_numpy()
#print(elemMasses)
#xSC = df['x_SCS'].to_numpy()
#print(xSC)

n = 4.37 #założenie

bPrzez2 = b/2

#Dzielę skrzydło (!) na 20 kawałków - 21 cięciw
# Ukłąd 1D współrzędnych zaczepiam w środku płata, tylko oś y

y = np.zeros(21) #wektor współrzędnych, które będą tworzyć paski
print("Współrzędne cięciw:\n")
for iCieciwa in range(0, 21):
    y[iCieciwa]=iCieciwa*(bPrzez2/20)
    print("y", iCieciwa," = ", y[iCieciwa])

#Rozkład cięciw dla b/2
cElips = 4*S/(math.pi*b)*(1 - (2*y/b)**2)**0.5
cTrapez = np.ones(21)*c
#Elementarna siłą nośna
#Płat eliptyczny
L_Elips = 4*L*n/(math.pi*b)*(1 - (2*y/b)**2)**0.5
#Płat trapezowy
L_Trapez = L/b

L_mean = np.mean([L_Elips, L_Trapez], axis=0)

fig = plt.figure(figsize=(8, 4))
plt.plot(y, cElips, '-o', color='orange', markersize=3, label='Plat eliptyczny')
plt.plot(y, cTrapez, '-o', color='blue', markersize=3, label='Plat trapezowy')
plt.legend()
plt.xlabel('y [m]')
plt.ylabel('c [m]')
plt.grid(True)
plt.savefig('Celip_Ctrap.png')
# Show the plot
plt.show()
plt.close()

# Second plot
fig = plt.figure(figsize=(8, 4))
plt.plot(y, L_mean, '-o', color='green', markersize=3)
plt.ylim(0, 2200)
plt.xlabel('y [m]')
plt.ylabel('L_jednostkowa [N/m]')
plt.grid(True)
plt.savefig('L_mean.png')
plt.show()
plt.close()

# stack the vectors horizontally to create a table
table = np.column_stack((y, cElips, cTrapez, L_mean))

# export the table to a CSV file
np.savetxt('rozkladShrenka.csv', table, delimiter=',', header='y [m],Eliptyczny, Trapezowy,Jednostkowa sila nosna [N/m]', comments='')











