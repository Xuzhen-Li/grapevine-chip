import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 读取数据
data = pd.read_csv('grape.chip.vcf.gz.freq2.frq.maf.bed', sep='\t')  # 替换为您的文件路径

# 按染色体和位置排序
data.sort_values(by=['CHROM', 'POS'], inplace=True)

# 美化直方图风格
sns.set(style="whitegrid")

# 绘制MAF的频率分布直方图
plt.figure(figsize=(10, 6))
sns.histplot(data['MAF'], bins=50, color='skyblue', kde=True)  # 使用seaborn绘图并添加核密度估计
plt.xlabel('MAF')
plt.ylabel('Frequency')
plt.title('Global Distribution of MAF')
plt.show()
