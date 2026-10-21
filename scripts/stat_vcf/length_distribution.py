###查看reads分布
## samtools view SAMPLE_A_cap.mapped.maponly.sorted.qF.sorted.cleaned.rmdup.MarkD.bam | awk '{print length($10)}' | sort | uniq -c > length_distribution.txt
##计算平均长度
##samtools view SAMPLE_X.mapped.bam | awk '{total += length($10); count++} END {print total/count}'

####单个样本图
import matplotlib.pyplot as plt

# 读取数据
counts = []
lengths = []
with open("<DATA_DIR>/bamlength.txt", "r") as file:
    for line in file:
        count, length = line.split()
        counts.append(int(count))
        lengths.append(int(length))

# 生成直方图
plt.bar(lengths, counts, color='blue')
plt.xlabel('Read Length')
plt.ylabel('Count')
plt.title('Read Length Distribution')
plt.show()



###对照样本图
import matplotlib.pyplot as plt

# 读取第一个样本的数据
counts_sample1 = []
lengths_sample1 = []
with open("SAMPLE_A.length_distribution.txt", "r") as file:
    for line in file:
        count, length = line.split()
        counts_sample1.append(int(count))
        lengths_sample1.append(int(length))

# 读取第二个样本的数据
counts_sample2 = []
lengths_sample2 = []
with open("SAMPLE_A_cap.length_distribution.txt", "r") as file:
    for line in file:
        count, length = line.split()
        counts_sample2.append(int(count))
        lengths_sample2.append(int(length))

# 生成直方图
plt.bar(lengths_sample1, counts_sample1, color='blue', alpha=0.5, label='Pre_capture')
plt.bar(lengths_sample2, counts_sample2, color='red', alpha=0.5, label='Post_Capture')
plt.xlabel('Read Length')
plt.ylabel('Count')
plt.title('')
plt.legend()
plt.show()



###美化版本
import matplotlib.pyplot as plt

# 设置图形的全局字体样式
plt.rcParams.update({
    'font.size': 20,
    'font.family': 'sans-serif',
    'legend.fontsize': 'medium'
})

# 读取第一个样本的数据
counts_sample1 = []
lengths_sample1 = []
with open("SAMPLE_B.length_distribution.txt", "r") as file:
    for line in file:
        count, length = line.split()
        counts_sample1.append(int(count))
        lengths_sample1.append(int(length))

# 读取第二个样本的数据
counts_sample2 = []
lengths_sample2 = []
with open("SAMPLE_B_cap.length_distribution.txt", "r") as file:
    for line in file:
        count, length = line.split()
        counts_sample2.append(int(count))
        lengths_sample2.append(int(length))

# 使用更加细致的颜色和透明度设置来生成直方图
plt.figure(figsize=(16, 6))  # 设置图像尺寸
plt.bar(lengths_sample1, counts_sample1, color='blue', alpha=0.7, label='Pre-capture', width=0.9)
plt.bar(lengths_sample2, counts_sample2, color='red', alpha=0.7, label='Post-capture', width=0.9)

# 设置图例、标题、轴标签
plt.xlabel('Read Length', fontsize=16)
plt.ylabel('Count', fontsize=16)
plt.title('', fontsize=16)
plt.legend()

# 设置网格线为更加柔和的颜色和样式
plt.grid(color='white', linestyle='-', linewidth=0.25, alpha=0.5)

# 调整轴的刻度大小
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)

# 输出图像到文件，这里设置为300 DPI的分辨率，适合高质量打印
plt.savefig("SAMPLE_Bread_length_distribution_comparison.png", dpi=300)

plt.show()  # 显示图像
