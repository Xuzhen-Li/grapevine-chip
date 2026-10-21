import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Adjust the filepath and sep parameter as per your file
data = pd.read_csv('<DATA_DIR>/stat_rate.txt', sep='\t', header=None)

data_long = data.melt(var_name='Group', value_name='Value')

# Rename the group labels
group_labels = ['Sample_Het', 'Site_Het', 'Sample_missing', 'Site_missing']  # Replace with your group names
data_long['Group'] = data_long['Group'].replace({i: group_labels[i] for i in range(len(group_labels))})

# GraphPad Prism style settings
sns.set(style="ticks", palette="pastel")
plt.figure(figsize=(8, 6))

# Create the boxplot with customized outlier representation
sns.boxplot(x='Group', y='Value', data=data_long, 
            boxprops=dict(alpha=.9),
            showmeans=True, 
            meanprops={"marker":"o", "markerfacecolor":"white", "markeredgecolor":"black", "markersize":"10"},
            flierprops=dict(marker='|', markerfacecolor='black', markersize=8))  # Outlier representation

# Enhance the plot aesthetics
plt.title(' ', fontsize=14, weight='bold')
plt.xlabel(' ', fontsize=12, weight='bold')
plt.ylabel('Rate', fontsize=12, weight='bold')
plt.xticks(fontsize=10, weight='bold')
plt.yticks(fontsize=10)
sns.despine(offset=10, trim=True)

plt.show()
