import seaborn as sns
import pandas as pd

path = 'xxxx.csv'
data = pd.read_csv(path)

# Define X and Y
x = data['x']
y = data['y']

# Plotting
sns.violinplot(x=x, y=y, data=data)
