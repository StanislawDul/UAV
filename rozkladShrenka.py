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
    else:
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

Vc = 35 #m/s - ustal dokładną wartość przy robienu obwiedni obciążeń!!
n = 5 #założenie jak wyżej!!!
C_L = 0.09 #jak wyżej!! Policzyć na podstawie Vc, S i MTOW

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
L_Elips = 4*L/(math.pi*b)*(1 - (2*y/b)**2)**0.5
#Płat trapezowy
L_Trapez = L/b

plt.plot(L_Elips, y)

# Show the plot
plt.show()










