import pandas as pd
import matplotlib.pyplot as plt

# 读取数据
data = pd.read_csv('postion_all.txt', sep='\t')

# 按染色体和位置排序
data.sort_values(by=['CHROM', 'POS'], inplace=True)

# 计算间隔距离
data['Interval'] = data.groupby('CHROM')['POS'].diff()

# 删除NaN值
data = data.dropna()

# 计算统计数据
stats = data.groupby('CHROM')['Interval'].agg(['max', 'min', 'mean']).reset_index()

# 显示统计数据
print(stats)

# 绘制柱状图
plt.figure(figsize=(10, 6))
plt.hist(data['Interval'], bins=100, range=(0, 10000), color='gray', alpha=0.5)  # 设置bins数量和范围

plt.xlabel('Interval Distance (bp)')
plt.ylabel('Count')
plt.title('Interval Distance Distribution')
plt.xlim(0, 10000)  # 设置x轴范围
plt.show()
