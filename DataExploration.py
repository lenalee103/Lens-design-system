# Import pandas
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
# Read data
lens = pd.read_excel('c:/Users/rf613258/Desktop/brain_and_b1/optical_lens_system/tolerance_analysis.xlsx')
#x = lens['RMSWavefront1']
#y = lens['EstimatedChange']
#colors = np.random.rand(1030)
#plt.scatter(x, y, c=colors, alpha=0.5)
#plt.show()
lens = lens.drop(lens.index[0])
lens.astype('float64')
print(lens.info())
print(lens.describe())
print(lens.dtypes)

corr = lens.corr()
#sns.heatmap(corr, xticklabels=corr.columns.values, yticklabels=corr.columns.values)
#plt.show()
print(corr)
