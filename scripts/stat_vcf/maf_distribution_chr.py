import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 读取数据
data = pd.read_csv('grape.chip.vcf.gz.freq2.frq.maf.bed', sep='\t')  # 替换为您的文件路径

# 设置图表风格
sns.set(style="whitegrid")

# 绘制箱线图
plt.figure(figsize=(12, 8))
sns.boxplot(x='CHROM', y='MAF', data=data, palette="Set2", whis=1.5)
#显示散点
#sns.stripplot(x='CHROM', y='MAF', data=data, color='black', size=3)

# 自定义须线和须末的样式
for i, artist in enumerate(plt.gca().artists):
    # 须线（whisker）
    artist.set_edgecolor('black')
    artist.set_linewidth(1.5)

    # 每个箱体有6个线条（2个须线，2个须末，1个箱体，1个中位数），找到须末线并进行设置
    for j in range(i*6, i*6+6):
        line = plt.gca().lines[j]
        line.set_color('black')
        line.set_mfc('black')
        line.set_mec('black')

# 设置坐标轴标签和标题
plt.xlabel('Chromosome', fontsize=16, weight='bold')
plt.ylabel('MAF', fontsize=16, weight='bold')
plt.title('MAF Distribution Across Chromosomes', fontsize=16, weight='bold')
plt.xticks(rotation=45, weight='bold')

# 显示图表
plt.show()
