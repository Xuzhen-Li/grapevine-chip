#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
两组条件对比的可视化脚本
运行：python mapped_rate.py
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib

# 设置全局字体和样式
plt.rcParams.update({
    'font.size': 12,
    'font.weight': 'bold',
    'axes.titlesize': 14,
    'axes.titleweight': 'bold',
    'axes.labelweight': 'bold',
    'figure.titlesize': 16,
    'figure.titleweight': 'bold'
})

# 从文件读取数据（仅两列）
def load_data(filename):
    """从文本文件加载样本数据"""
    df = pd.read_csv(filename, sep=r'\s+', header=None,
                     names=['Sample', 'Cond1', 'Cond2'])
    if len(df.columns) != 3:
        raise ValueError("数据文件应该包含3列：样本ID和两个条件值")
    return df

# 主函数
def visualize_data(input_file, output_file="mapped_rate.pdf"):
    """可视化样本数据并保存为PDF"""
    try:
        df = load_data(input_file)
        print(f"成功加载数据: {len(df)} 个样本")
    except Exception as e:
        print(f"数据加载错误: {e}")
        return

    fig, ax = plt.subplots(figsize=(6, 8))

    # 仅两组
    condition_colors = ['#1f77b4', '#1f77b4']
    condition_labels = ['Capture-in-solution(Amplified)', 'dsDNA-Probe']

    # 箱线图背景（两组）
    sns.boxplot(data=df[['Cond1', 'Cond2']],
                width=0.3,
                showfliers=False,
                boxprops=dict(alpha=0.3),
                palette=['#FF5252', '#66BB6A'])

    # 连线 & 散点（仅 0→1）
    for idx, row in df.iterrows():
        color = '#66BB6A' if row['Cond2'] >= row['Cond1'] else '#FF5252'
        plt.plot([0, 1], [row['Cond1'], row['Cond2']],
                 color=color, linewidth=1.5, alpha=0.8)
        for i, cond in enumerate(['Cond1', 'Cond2']):
            plt.scatter(i, row[cond], color=condition_colors[i],
                        s=60, edgecolor='black', zorder=3)

    plt.title('Mapped Rate', pad=20)
    plt.ylabel('Mapped rate', labelpad=15)
    plt.xlabel('Condition', labelpad=15)
    plt.xticks([0, 1], condition_labels)

    # 图例
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], color='#66BB6A', lw=4, label='Increase'),
        Line2D([0], [0], color='#FF5252', lw=4, label='Decrease')
    ]
    plt.legend(handles=legend_elements, loc='upper left', frameon=True)

    # 美化
    for spine in ax.spines.values():
        spine.set_linewidth(1.5)
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()

    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"可视化结果已保存至: {output_file}")
    plt.close()

if __name__ == "__main__":
    input_filename = "data_mappedrate.txt"  # 三列：样本ID  Cond1  Cond2
    visualize_data(input_filename)