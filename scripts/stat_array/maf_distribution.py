import pandas as pd
import matplotlib.pyplot as plt
##导入csv
df = pd.read_csv('<DATA_DIR>/maf.csv', header=None, names=['Numbers'])
# 将数字分组
bins = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]
groups = pd.cut(df['Numbers'], bins=bins, include_lowest=True)
# 统计数字分布情况
result = groups.value_counts(sort=False)
# 查看结果
print(result) 
# 绘制柱状图
plt.bar(result.index.astype(str), result.values)
# 设置图表标题和坐标轴标签
plt.title('MAF Distribution of Numbers')
plt.xlabel('MAF Groups')
plt.ylabel('Count')
# 显示图表
plt.show()
