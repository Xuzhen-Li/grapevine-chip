import pandas as pd
import matplotlib.pyplot as plt
##导入csv
df = pd.read_csv('<DATA_DIR>/site.csv', header=None, names=['Numbers'])
# 将数字分组
bins = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9 ,10, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000]
groups = pd.cut(df['Numbers'], bins=bins, include_lowest=True)
# 统计数字分布情况
result = groups.value_counts(sort=False)
# 查看结果
print(result) 
# 绘制柱状图
plt.bar(result.index.astype(str), result.values)
# 调整字体大小
#plt.rcParams.update({'font.size': 2})
# 调整横轴标签的字体大小
plt.xticks(fontsize=4)
# 设置图表标题和坐标轴标签
plt.title('site Distribution of Numbers')
plt.xlabel('1vN Groups')
plt.ylabel('site Count')
# 显示图表
plt.show()