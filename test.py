from matplotlib import pyplot as plt
import numpy as np
import math
import pandas as pd

x = np.linspace(-10, 10, 1001)
y = x**2

ax = plt.plot()
ax.plot(x, y)

matplotlib.use('Agg')
plt.savefig('my_plot.png')