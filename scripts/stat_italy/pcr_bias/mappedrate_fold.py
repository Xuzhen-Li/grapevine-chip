#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNS-grade box+strip plot：Mapped rate fold (Post_PCR / Pre_PCR)
运行：python fold_boxplot_CNS.py
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. 读取数据
df = pd.read_csv('mappedrate_fold.txt', sep=r'\s+',
                 names=['Sample', 'Pre_Capture', 'Post_Capture'])

# 2. 长表转换
df_melt = df.melt(id_vars='Sample',
                  value_vars=['Pre_Capture', 'Post_Capture'],
                  var_name='Method', value_name='Fold_change')

# 3. CNS 全局样式
plt.style.use('default')
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica'],
    'font.size': 8,
    'axes.linewidth': 0.5,
    'axes.titlesize': 9,
    'axes.titleweight': 'bold',
    'axes.labelsize': 9,
    'axes.labelweight': 'bold',
    'xtick.major.width': 0.5,
    'ytick.major.width': 0.5,
    'xtick.direction': 'in',
    'ytick.direction': 'in',
    'savefig.dpi': 600,
    'savefig.transparent': True,
})

# Paul Tol 2023 色盲友好配色
cns_palette = {'Pre_Capture': '#4472A4',   # 柔和蓝
               'Post_Capture': '#E15759'}  # 柔和红

# 4. 绘图（单栏宽度）
fig, ax = plt.subplots(figsize=(2.2, 3.3))

# 箱线图
sns.boxplot(data=df_melt, x='Method', y='Fold_change',
            width=0.45, showfliers=False,
            palette=cns_palette,
            boxprops=dict(alpha=0.65, linewidth=0.5),
            whiskerprops=dict(linewidth=0.5),
            medianprops=dict(color='black', linewidth=1))

# 散点（strip）
sns.stripplot(data=df_melt, x='Method', y='Fold_change',
              palette=cns_palette,
              size=3.5, alpha=0.9, edgecolor='black',
              linewidth=0.25, jitter=0.12, zorder=3)

# 5. 标题与轴标签
ax.set_title('Mapped rate fold (Post_PCR / Pre_PCR)', fontsize=9, pad=6, weight='bold')
ax.set_xlabel('Method', fontsize=9, weight='bold', labelpad=4)
ax.set_ylabel('Fold change', fontsize=9, weight='bold', labelpad=4)

# 6. 去边框
sns.despine(ax=ax, top=True, right=True)

# 7. 保存
plt.tight_layout()
plt.savefig('mappedrate_fold.pdf', dpi=600, bbox_inches='tight')
plt.close()
print('已保存 mappedrate_fold.pdf')