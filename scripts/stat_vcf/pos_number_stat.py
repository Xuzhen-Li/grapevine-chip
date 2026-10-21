import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the data
data = pd.read_csv('postion.txt', sep='\t')  # Replace with your file path

# Count positions per chromosome
position_counts = data['CHROM'].value_counts().sort_index()

# 转换为DataFrame以便输出
chromosome_stats = pd.DataFrame(position_counts).reset_index()
chromosome_stats.columns = ['Chromosome', 'Number of Positions']

# 显示统计表格
print(chromosome_stats)

# Improve plot style for a GraphPad Prism-like appearance
sns.set(style="whitegrid")
plt.figure(figsize=(8, 6))
ax = position_counts.plot(kind='bar', color='skyblue', alpha=0.7)
ax.set_xlabel('Chromosome', fontsize=12, weight='bold')
ax.set_ylabel('Number of Positions', fontsize=12, weight='bold')
ax.set_title('Number of Positions per Chromosome', fontsize=14, weight='bold')
plt.xticks(rotation=45, ha='right', fontsize=10)
plt.yticks(fontsize=10)
sns.despine()  # Removes top and right border

# Show the plot
plt.tight_layout()
plt.show()
