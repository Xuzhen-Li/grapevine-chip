import matplotlib.pyplot as plt
import pandas as pd

# 读取CSV文件
file_path = 'pca2449_203985.csv'
df = pd.read_csv(file_path, sep=',')

# 确定颜色和标记字典是否已经准备好
# 为每个类别定义颜色，确保这些颜色与提供的图样一致
colors = {
    'CG1': '#FF0000',  # Red
    'CG2': '#0000FF',  # Blue
    'CG3': '#008000',  # Green
    'CG4': '#800080',  # Purple
    'CG5': '#00FFFF',  # Cyan
    'CG6': '#FF00FF',  # Magenta
    'OUT': '#FFFF00',  # Yellow
    'W-Ad': '#000000',  # Black
    'C-Ad': '#000000',  # Black
    'WEE1': '#FFA500',  # Orange, corresponding to Syl-E1
    'WEE2': '#FFC0CB',  # Pink, corresponding to Syl-E2
    'WWE1': '#00FF00',  # Lime, corresponding to Syl-W1
    'WWE2': '#A52A2A',  # Brown, corresponding to Syl-W2
}

# 为每个类别定义标记，可以根据图样进行修改
markers = {
    'CG1': 'o', 'CG2': 's', 'CG3': '^', 'CG4': 'D',
    'CG5': '>', 'CG6': '<', 'OUT': 'p', 'W-Ad': '*', 'C-Ad': '*',
    'WEE1': 'X', 'WEE2': 'd', 'WWE1': '|', 'WWE2': '_'
}

# 创建散点图
for category, group in df.groupby('Grp'):
    plt.scatter(group['PC1(6.12%)'], group['PC2(2.42%)'], 
                color=colors.get(category, 'gray'), 
                marker=markers.get(category, 'o'), 
                alpha=0.5, 
                label=category)

# 自定义图表
plt.xlabel('PC 1 (6.12%)')
plt.ylabel('PC 2 (2.42%)')
plt.title('PCA Plot')
plt.legend(title='Group', bbox_to_anchor=(1.05, 1), loc='upper left')

# 设置x轴和y轴的范围
plt.xlim(-0.025, 0.05)  # 例如：x轴范围从-0.1到0.1
plt.ylim(-0.01, 0.011)  # 例如：y轴范围从-0.1到0.1

# 调整布局以为图例留出空间
plt.tight_layout()

# 保存图表的路径和文件名应正确指定
plt.savefig('PCA_Plot.png', bbox_inches='tight')

# 显示图表
plt.show()
