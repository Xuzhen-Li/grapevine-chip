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

# 从文件读取数据
def load_data(filename):
    """从文本文件加载样本数据"""
    # 使用正则表达式匹配任何空白分隔符
    df = pd.read_csv(filename, sep=r'\s+', header=None, 
                    names=['Sample', 'Cond1', 'Cond2', 'Cond3', 'Cond4'])
    
    # 验证数据列数
    if len(df.columns) != 5:
        raise ValueError("数据文件应该包含5列：样本ID和4个条件值")
    
    return df

# 主函数
def visualize_data(input_file, output_file="low_capeff_rate.pdf"):
    """可视化样本数据并保存为PDF"""
    # 1. 加载数据
    try:
        df = load_data(input_file)
        print(f"成功加载数据: {len(df)} 个样本")
    except Exception as e:
        print(f"数据加载错误: {e}")
        return
    
    # 2. 创建可视化
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # 配置颜色方案
    condition_colors = ['#1f77b4', '#1f77b4', '#1f77b4', '#1f77b4']  # 所有点使用相同颜色
    condition_labels = ['Shotgun', 'Capture-in-solution(Shotgun)', 
                        'Amplification', 'Capture-in-solution(Amplified)']
    
    # 先绘制箱线图作为背景
    sns.boxplot(data=df[['Cond1', 'Cond2', 'Cond3', 'Cond4']], 
                width=0.3, 
                showfliers=False,
                boxprops=dict(alpha=0.3),
                palette=['#FF5252', '#FF5252', '#66BB6A', '#66BB6A'])
    
    # 3. 绘制每个样本的数据点
    for idx, row in df.iterrows():
        # 根据数值变化确定连线颜色（增加为绿线，减少为红线）
        # 第一组条件：Cond1->Cond2
        color12 = '#66BB6A' if row['Cond2'] >= row['Cond1'] else '#FF5252'
        plt.plot([0, 1], [row['Cond1'], row['Cond2']], 
                 color=color12, linewidth=1.5, alpha=0.8)
        
        # 第二组条件：Cond3->Cond4
        color34 = '#66BB6A' if row['Cond4'] >= row['Cond3'] else '#FF5252'
        plt.plot([2, 3], [row['Cond3'], row['Cond4']], 
                 color=color34, linewidth=1.5, alpha=0.8)
        
        # 各个数据点
        for i, cond in enumerate(['Cond1', 'Cond2', 'Cond3', 'Cond4']):
            plt.scatter(i, row[cond], color=condition_colors[i], 
                        s=60, edgecolor='black', zorder=3)  # 确保点在连接线上方
    
    # 4. 添加标题和标签
    plt.title('Low Endogenous DNA Samples Capture Efficiency', pad=20)
    plt.ylabel('Capture Efficiency Rate (Target reads / Mapped reads)', labelpad=15)
    plt.xlabel('Condition', labelpad=15)
    
    # 设置x轴刻度和标签
    plt.xticks([0, 1, 2, 3], condition_labels)
    
    # 5. 添加图例
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], color='#66BB6A', lw=4, label='Increase'),
        Line2D([0], [0], color='#FF5252', lw=4, label='Decrease')
    ]
    plt.legend(handles=legend_elements, loc='upper left', frameon=True)
    
    # 6. 美化图表
    for spine in ax.spines.values():
        spine.set_linewidth(1.5)
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()
    
    # 7. 保存图像
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"可视化结果已保存至: {output_file}")
    plt.close()

# 主程序入口
if __name__ == "__main__":
    # 从文件读取数据并生成可视化
    input_filename = "data_capeff_low.txt"  # 您的数据文件路径
    visualize_data(input_filename)