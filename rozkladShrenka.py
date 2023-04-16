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
    print(variableName[iVar], " = ", variableValue[iVar])

df = pd.read_csv('Mass_Table.xlsx')



