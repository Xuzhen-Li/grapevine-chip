



sed 's/\t/ /g'  k2s.Q > k2.Q 
sed 's/\t/ /g'  k3s.Q > k3.Q 
sed 's/\t/ /g'  k4s.Q > k4.Q 
sed 's/\t/ /g'  k5s.Q > k5.Q 
sed 's/\t/ /g'  k6s.Q > k6.Q 
sed 's/\t/ /g'  k7s.Q > k7.Q 
sed 's/\t/ /g'  k8s.Q > k8.Q 


file_path <- "k2.Q"
    data2 <- read.table(file_path, header=FALSE, sep=" ", stringsAsFactors = FALSE)
    head(data2)
    str(data2)
    data_numeric <- apply(data2, 2, function(x) as.numeric(as.character(x)))
    # 检查是否有NA值
na_count <- sum(is.na(data_numeric))
if (na_count > 0) {
  cat("Found", na_count, "NA values in the dataset. Further investigation required.\n")
}
# 将修正后的数据保存为新文件
write.table(as.data.frame(data_numeric), "nk2.Q", row.names=FALSE, col.names=FALSE, sep=" ", quote=FALSE)



    
    file_path <- "k3.Q"
    data3 <- read.table(file_path, header=FALSE, sep=" ", stringsAsFactors = FALSE)
    head(data3)
    str(data3)
    data_numeric <- apply(data3, 2, function(x) as.numeric(as.character(x)))
    # 检查是否有NA值
na_count <- sum(is.na(data_numeric))
if (na_count > 0) {
  cat("Found", na_count, "NA values in the dataset. Further investigation required.\n")
}
# 将修正后的数据保存为新文件
write.table(as.data.frame(data_numeric), "nk3.Q", row.names=FALSE, col.names=FALSE, sep=" ", quote=FALSE)

    file_path <- "k4.Q"
    data4 <- read.table(file_path, header=FALSE, sep=" ", stringsAsFactors = FALSE)
    head(data4)
    str(data4)


    file_path <- "k5.Q"
    data5 <- read.table(file_path, header=FALSE, sep=" ", stringsAsFactors = FALSE)
    head(data5)
    str(data)


    file_path <- "k6.Q"
    data6 <- read.table(file_path, header=FALSE, sep=" ", stringsAsFactors = FALSE)
    head(data6)
    str(data6)


    file_path <- "k7.Q"
    data7 <- read.table(file_path, header=FALSE, sep=" ", stringsAsFactors = FALSE)
    head(data7)
    str(data7)


    file_path <- "k8.Q"
    data8 <- read.table(file_path, header=FALSE, sep=" ", stringsAsFactors = FALSE)
    head(data8)
    str(data8)

    





# 加载所需的库
library(pophelper)

# 读取转换为数值形式后的Q文件
file_path <- "nk2.Q"
data_numeric <- read.table(file_path, header=FALSE, sep=" ", stringsAsFactors=FALSE)

# 转换数据框，确保所有列都是数值型
data_df <- as.data.frame(data_numeric)

# 假设样本ID在另一个文件中，按照相同的顺序
sample_ids <- read.table("id_only.txt", header=FALSE, stringsAsFactors=FALSE)$V1

# 设置样本ID为数据框的行名
rownames(data_df) <- sample_ids

# 如果有分组信息，也读取分组信息
group_info <- read.table("grp.pophelper", header=FALSE, sep=",", col.names=c("SampleID", "Group"), stringsAsFactors=FALSE)

# 创建qlist，用于pophelper绘图
qlist <- list(K2=data_df)
names(qlist) <- "K2"  # 给qlist中的元素命名

# 将qlist转换为pophelper可以识别的格式
qlist <- as.qlist(qlist)

pdf("k2_structure_plot_with_groups.pdf", width=11, height=8.5)
    plotQ(qlist, exportpath=getwd())
    dev.off()





#########
# 加载pophelper库
library(pophelper)

# 假设你的.Q文件在当前工作目录的"structure_results"文件夹中
# 并且命名为"K2_structure_output_1.Q", "K3_structure_output_1.Q", ..., "K8_structure_output_1.Q"
# 同时你有一个叫做"groupinfo.csv"的文件，其中包含了每个样本的ID和对应的组

# 生成.Q文件的路径列表
qfiles <- list.files(path="./", pattern="n*.Q", full.names=TRUE)

# 使用readQ函数读取.Q文件
qlist <- lapply(qfiles, readQ)

# 读取组信息
groupinfo <- read.csv("grp.pophelper", header=TRUE)

# 遍历每个K值的结果
for (i in seq_along(qlist)) {
  # 为每个K值创建一个新的pdf文件
  pdf(paste0("K", i + 1, "_structure_plots.pdf"), width=11, height=8.5)
  
  # 从qlist中获取当前的Q矩阵
  qmatrix <- qlist[[i]]$Q
  
  # 将Q矩阵和组信息按照样本ID合并
  qmatrix <- merge(qmatrix, groupinfo, by.x="ind", by.y="ID", all.x=TRUE)
  
  # 按组排序Q矩阵
  qmatrix <- qmatrix[order(qmatrix$Group), ]
  
  # 为当前K值按组绘制结构图
  plotlist <- plotQ(qmatrix, imgoutput="join", returnplotlist=TRUE)
  
  # 打印所有图形
  invisible(lapply(plotlist, print))
  
  # 关闭pdf文件
  dev.off()
}



######3放弃了


# 加载必要的包
library(RColorBrewer)
library(plyr)
library(tidyr)
library(ggplot2)
library(dplyr)
require(ggplot2) 

# 读取数据，因为没有表头，我们需要手动指定列名
data <- read.table("k3_2449_grp.txt", header=FALSE, sep="\t", col.names=c("ID", "K1", "K2", "K3", "Group"))
# 假设你的原始数据框架叫做data，并且它已经被读入R中
# 首先确保数据是按照分组和ID排序的
data <- data %>% arrange(Group)

# 转换数据框架为长格式
data_long <- pivot_longer(data, cols = c(K1, K2, K3), names_to = "K", values_to = "Proportion")

# 绘图，这次我们会调整图表的字号和分辨率
ggplot(data_long, aes(x=reorder(ID, Group), y=Proportion, fill=K)) +
  geom_bar(stat="identity", position="stack") +
  xlab("Sample") + ylab("Admixture Proportion") +
  scale_fill_manual(values=c("K1"="blue", "K2"="purple", "K3"="red")) +
  theme_minimal() +
  theme(axis.text.x = element_text(size=6), axis.title=element_text(size=10)) # 调整字号

# 保存图表，提高分辨率
ggsave("admixture_results_high_res.pdf", width=12, height=2.5, dpi=600)




library(ggplot2)
library(tidyr)
library(dplyr)

# 读取数据
data <- read.table("k3_2449_grp.txt", header = FALSE, col.names = c("ID", "K1", "K2", "K3", "Group"))

# 转换数据为长格式
data_long <- pivot_longer(data, cols = K1:K3, names_to = "Ancestry", values_to = "Proportion")

# 绘制ADMIXTURE图
ggplot(data_long, aes(x = reorder(ID, -Proportion), y = Proportion, fill = Ancestry)) +
  geom_bar(stat = "identity", position = "fill") +
  facet_wrap(~ Group, scales = "free_x", nrow = 1) +
  scale_fill_brewer(palette = "Set1") +
  theme_minimal() +
  theme(axis.text.x = element_blank(), axis.ticks.x = element_blank(), legend.position = "bottom") +
  labs(x = NULL, y = "Ancestry Proportion", fill = "Ancestry") +
  guides(fill = guide_legend(reverse = TRUE))

# 保存图片到PDF文件，这里设置尺寸可能需要根据你的具体需求调整
ggsave("admixture_plot.pdf", width = 20, height = 5)


library(ggplot2)
library(tidyr)
library(dplyr)
library(RColorBrewer)

# 设置颜色，这里设置了8种，足够用于k2到k8的任何情况
# 根据你的需求，你可以选择其他的颜色或者调色板
color_palette <- brewer.pal(8, "Set1")

# 准备一个循环处理k2到k8
for (k in 2:8) {
  # 构造文件名
  file_name <- paste0("k", k, "_2449_grp.txt")
  
  # 读取数据
  data <- read.table(file_name, header = FALSE, col.names = c("ID", paste0("K", 1:k), "Group"))
  
  # 转换数据为长格式
  data_long <- pivot_longer(data, cols = starts_with("K"), names_to = "Ancestry", values_to = "Proportion")
  
  # 绘制ADMIXTURE图
  plot <- ggplot(data_long, aes(x = reorder(ID, -Proportion), y = Proportion, fill = Ancestry)) +
    geom_bar(stat = "identity", position = "fill") +
    scale_fill_manual(values=color_palette[1:k]) +
    facet_wrap(~ Group, scales = "free_x", nrow = 1) +
    theme_minimal() +
    theme(axis.text.x = element_blank(), axis.ticks.x = element_blank(), legend.position = "bottom") +
    labs(x = NULL, y = "Ancestry Proportion", fill = "Ancestry") +
    guides(fill = guide_legend(reverse = TRUE))
  
  # 保存图片到PDF文件，这里设置尺寸可能需要根据你的具体需求调整
  ggsave(paste0("admixture_plot_k", k, ".pdf"), plot=plot, width = 20, height = 5)
}

检查非数字
# 读取数据文件，假设列名为ID, K1, K2, K3, K4, K5, Group
# 请将文件名更改为实际的文件名
data <- read.table("k5_2449_grp.txt", header = FALSE, col.names = c("ID", "K1", "K2", "K3", "K4", "K5", "Group"))

# 检查前几行的K5列数据
head(data$K5)

# 检查K5列的数据类型
class(data$K5)

# 检查K5列中是否有非数值的值
sum(!is.na(as.numeric(as.character(data$K5)))) != length(data$K5)

# 如果上面的sum命令返回TRUE，表示有非数值存在，可以进一步检查哪些值是非数值的
data$K5[!is.na(as.numeric(as.character(data$K5))) == FALSE]
