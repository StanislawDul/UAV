import matplotlib.pyplot as plt
import numpy as np
import math
import pandas as pd

x = np.linspace(0, 10, 100)
jedynki = np.ones(100)
dwojki = np.ones(100)*2
srednia = np.mean([jedynki, dwojki], axis=0)

plt.plot(x, jedynki)
plt.plot(x, dwojki)
plt.show()
plt.close()