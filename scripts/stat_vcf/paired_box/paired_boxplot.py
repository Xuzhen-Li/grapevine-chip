# Adjusting the boxplot to have semi-transparent boxes to prevent hiding the scatter points

# Re-importing the necessary libraries and defining the data for plotting
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Re-read the data into a DataFrame
data = pd.read_csv('<DATA_DIR>/figure_adna_versus.txt', sep='\s+', header=None, thousands=',', names=['ID', 'First Treatment', 'Second Treatment'])

# Define upregulated and downregulated samples
upregulated = data['First Treatment'] < data['Second Treatment']
downregulated = data['First Treatment'] > data['Second Treatment']

# Set plot size larger to minimize overlapping
plt.figure(figsize=(12, 8))

# Set the style of seaborn to white background
sns.set(style="whitegrid")

# Plotting upregulated samples in green with increased alpha for transparency
for i in np.where(upregulated)[0]:
    plt.plot([0, 1], data.iloc[i, 1:3], color='green', marker='o', markersize=5, markeredgecolor='black', alpha=0.7)

# Plotting downregulated samples in red with increased alpha for transparency
for i in np.where(downregulated)[0]:
    plt.plot([0, 1], data.iloc[i, 1:3], color='red', marker='o', markersize=5, markeredgecolor='black', alpha=0.7)

# Annotating sample names on the first treatment points
#for i, row in data.iterrows():
 #   plt.text(-0.05, row['First Treatment'], row['ID'], fontsize=9, ha='right')
#for i, row in data.iterrows():
   # plt.plot([0, 1], [row['First Treatment'], row['Second Treatment']], '-o', c='black', alpha=0.7)
    # 为了避免标签重叠，我们在标签旁边绘制一条小线，并在这条线的末端添加文本
   # label_x = -0.2 - 0.05 * i  # 每个标签的x位置稍微有所不同，以避免重叠
   # label_y = row['First Treatment']
   # plt.plot([label_x + 0.05, label_x], [label_y, label_y], c='black', alpha=0.7)
   # plt.text(label_x, label_y, row['ID'], verticalalignment='center', horizontalalignment='right', fontsize=9, color='black')


# Plot the boxplot with seaborn and make boxes semi-transparent
sns.boxplot(data=data[['First Treatment', 'Second Treatment']], palette=['skyblue', 'lightgrey'], width=0.2, showcaps=True, boxprops=dict(alpha=0.4))

# Setting titles and labels with bold font
plt.title('10x VS 20x sequecing(covered panel)', fontsize=16, weight='bold')
plt.ylabel('Reads Counts', fontsize=14, weight='bold')
plt.xlabel('Treatment Stage', fontsize=14, weight='bold')
plt.xticks(ticks=[0, 1], labels=['10x', '20x'], fontsize=12, weight='bold')
plt.yticks(fontsize=12, weight='bold')

# Remove top and right border for cleaner look
sns.despine()

# Show the final result with a tight layout
plt.tight_layout()
plt.show()  # Display the plot








#########5个处理###########
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# 假设您的文件已正确格式化并且每行有六列数据：ID, Treatment1, Treatment2, Treatment3, Treatment4, Treatment5
# 根据您的文件实际情况，可能需要调整sep参数，这里假设是用空格分隔的
data = pd.read_csv('<DATA_DIR>/figure_specimen_versus.txt', sep='\s+', header=None, names=['ID', 'First Treatment', 'Second Treatment', 'Third Treatment', 'Fourth Treatment', 'Fifth Treatment'])

# 定义上调和下调样本
# 这里的逻辑可能需要根据您的具体科研需求进行调整
upregulated = (data['First Treatment'] < data['Second Treatment']) | (data['Second Treatment'] < data['Third Treatment']) | \
              (data['Third Treatment'] < data['Fourth Treatment']) | (data['Fourth Treatment'] < data['Fifth Treatment'])
downregulated = (data['First Treatment'] > data['Second Treatment']) | (data['Second Treatment'] > data['Third Treatment']) | \
                (data['Third Treatment'] > data['Fourth Treatment']) | (data['Fourth Treatment'] > data['Fifth Treatment'])

# 设置图表大小
plt.figure(figsize=(12, 8))
sns.set(style="whitegrid")

# 绘制上调和下调样本
for condition in range(1, 6):  # 循环通过所有5个处理
    for i in np.where(upregulated)[0]:
        plt.plot(np.arange(0, 5), data.iloc[i, 1:6], color='green', marker='o', markersize=5, markeredgecolor='black', alpha=0.7)
    for i in np.where(downregulated)[0]:
        plt.plot(np.arange(0, 5), data.iloc[i, 1:6], color='red', marker='o', markersize=5, markeredgecolor='black', alpha=0.7)

# 绘制线条
for i in range(len(data)):
    for j in range(1, 5):  # 这里是因为我们有5个处理，所以查看4个节点之间的变化
        # 如果当前节点的值小于下一个节点的值，使用绿色表示上升
        if data.iloc[i, j] < data.iloc[i, j+1]:
            plt.plot([j-1, j], data.iloc[i, j:j+2], color='green', marker='o', markersize=5, markeredgecolor='black', alpha=0.7)
        # 否则，使用红色表示下降
        else:
            plt.plot([j-1, j], data.iloc[i, j:j+2], color='red', marker='o', markersize=5, markeredgecolor='black', alpha=0.7)

# 绘制箱形图
sns.boxplot(data=data.iloc[:, 1:6], palette=['skyblue', 'lightgrey', 'lightgreen', 'lightcoral', 'lightyellow'], width=0.2, showcaps=True, boxprops=dict(alpha=0.5))

# 设置标题和标签
plt.title('Specimen test(reads on panel))', fontsize=16, weight='bold')
plt.ylabel('Reads count(M)', fontsize=14, weight='bold')
plt.xlabel('Treatment Stage', fontsize=14, weight='bold')
plt.xticks(ticks=np.arange(0, 5), labels=['20x', '10x 5y-DNA', '10x 5y-DNA-cap', '10x 5y-sample', '10x 5y-sample-cap'], fontsize=12, weight='bold')
plt.yticks(fontsize=12, weight='bold')

# 移除上方和右方边框
sns.despine()

# 显示图表
plt.tight_layout()
plt.show()








##########3个处理############
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# 这里您需要根据实际的文件路径和文件名来调整
# 假设您的文件中数据是用空格分隔的
data = pd.read_csv('figure_specimen_versus.txt', sep='\s+', header=None, names=['ID', 'First Treatment', 'Second Treatment', 'Third Treatment'])

# 设置图表大小
plt.figure(figsize=(12, 8))
sns.set(style="whitegrid")

# 绘制线条
for i in range(len(data)):
    for j in range(1, 3):  # 由于现在只有三个处理，所以我们只需要检查两个节点之间的变化
        # 如果当前节点的值小于下一个节点的值，使用绿色表示上升
        if data.iloc[i, j] < data.iloc[i, j+1]:
            plt.plot([j-1, j], data.iloc[i, j:j+2], color='green', marker='o', markersize=5, markeredgecolor='black', alpha=0.7)
        # 否则，使用红色表示下降
        else:
            plt.plot([j-1, j], data.iloc[i, j:j+2], color='red', marker='o', markersize=5, markeredgecolor='black', alpha=0.7)

# 绘制箱形图
sns.boxplot(data=data.iloc[:, 1:4], palette=['skyblue', 'lightgrey', 'lightgreen'], width=0.2, showcaps=True, boxprops=dict(alpha=0.5))

# 设置标题和标签
plt.title('Specimen test(Total reads)', fontsize=16, weight='bold')
plt.ylabel('Reads counts', fontsize=14, weight='bold')
plt.xlabel('Treatment Stage', fontsize=14, weight='bold')
plt.xticks(ticks=np.arange(0, 3), labels=['10x', '10x 5y-sample', '10x-5y-sample-cap'], fontsize=12, weight='bold')
plt.yticks(fontsize=12, weight='bold')

# 移除上方和右方边框
sns.despine()

# 显示图表
plt.tight_layout()
plt.show()




###美化
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# 加载数据
data = pd.read_csv('figure_specimen_versus.txt', sep='\s+', header=None, names=['ID', 'First Treatment', 'Second Treatment', 'Third Treatment'])

# 设置图表的风格和颜色方案
sns.set_theme(style="ticks", palette="pastel")

# 设置图表大小和字体
plt.figure(figsize=(8, 6))
plt.rc('font', size=12)  # 控制默认字体大小
plt.rc('axes', titlesize=14)  # 控制轴标题的大小
plt.rc('axes', labelsize=12)  # 控制x和y轴标签的大小
plt.rc('xtick', labelsize=12)  # 控制x轴刻度标签的大小
plt.rc('ytick', labelsize=12)  # 控制y轴刻度标签的大小
plt.rc('legend', fontsize=12)  # 控制图例的大小
plt.rc('figure', titlesize=16)  # 控制图形标题的大小

# 绘制线条
for i in range(len(data)):
    for j in range(1, 3):  # 由于现在只有三个处理，所以我们只需要检查两个节点之间的变化
        if data.iloc[i, j] < data.iloc[i, j+1]:
            plt.plot([j-1, j], data.iloc[i, j:j+2], color='g', marker='o', markersize=5, linestyle='-', linewidth=2)
        else:
            plt.plot([j-1, j], data.iloc[i, j:j+2], color='r', marker='o', markersize=5, linestyle='-', linewidth=2)

# 绘制箱形图
sns.boxplot(data=data.iloc[:, 1:4], width=0.3, showfliers=False, boxprops=dict(alpha=.3))

# 设置边框的颜色和粗细
plt.gca().spines['top'].set_color('black')
plt.gca().spines['top'].set_linewidth(2)
plt.gca().spines['right'].set_color('black')
plt.gca().spines['right'].set_linewidth(2)
plt.gca().spines['left'].set_color('black')
plt.gca().spines['left'].set_linewidth(2)
plt.gca().spines['bottom'].set_color('black')
plt.gca().spines['bottom'].set_linewidth(2)

# 设置标题和标签
plt.title('Specimen test (Total reads)')
plt.ylabel('Reads counts')
plt.xlabel('Treatment Stage')
plt.xticks(ticks=np.arange(0, 3), labels=['10x', '10x 5y-sample', '10x-5y-sample-cap'])

# 设置刻度的样式
plt.tick_params(axis='both', which='major', labelsize=12, direction='out', length=6, width=2)

# 保存为PDF
plt.tight_layout()
plt.savefig('figure_specimen_versus.pdf', format='pdf', bbox_inches='tight')
plt.show()

