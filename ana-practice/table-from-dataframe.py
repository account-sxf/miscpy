import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#make this example reproducible
np.random.seed(0)

#define figure and axes
fig, ax = plt.subplots()

#hide the axes
fig.patch.set_visible(False)
ax.axis('off')
ax.axis('tight')

#create data
df = pd.DataFrame(np.random.randn(20, 2), columns=['First', 'Second'])

#create table
table = ax.table(cellText=df.values, colLabels=df.columns, loc='center')

#display table
fig.tight_layout()
plt.show()