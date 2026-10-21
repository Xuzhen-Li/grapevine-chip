## stat array
## 从 <N_TOTAL> 个位点里提取了 <N_SITES> 个点
### plink转格式，算het，freq，hardy，missing, py统计画图
### vcftools --keep 提取<N_SAMPLES> <DATA_DIR>/stat_vcf$ vcftools --gzvcf grape.chip.vcf.gz --keep <N_SAMPLES>.keep.list --recode --recode-INFO-all --stdout | gzip -c > <N_SAMPLES>.vcf.gz
## 跑pca admixture treemix

## 统计一下数字
### snp calling
```bash
for i in `ls *_r2.fq.gz | sed s/_r2.fq.gz//g`;
 do
 echo "gatk --java-options \"-Djava.io.tmpdir=./temp -Xms4G -Xmx4G\" HaplotypeCaller  -R ../../../genome/VS1.final.fa  -I ${i}.mapped.maponly.sorted.qF.sorted.cleaned.rmdup.MarkD.bam  -ERC GVCF -A StrandOddsRatio -A Coverage -A QualByDepth -A FisherStrand -A MappingQualityRankSumTest -A ReadPosRankSumTest -A RMSMappingQuality -O ${i}.g.vcf.gz" > ${i}.sh
done

for i in `ls *_r2.fq.gz | sed s/_r2.fq.gz//g`;
 do
 nohup bash ${i}.sh &
 done


4.0以后必须先combine别忘了索引
gatk IndexFeatureFile -F <DATA_DIR>/SAMPLE_01.raw.gvcf.gz 
# ...（同上，对其余样本重复 9 行）
gatk IndexFeatureFile -F <DATA_DIR>/SAMPLE_11.raw.gvcf.gz
# ...（同上，对其余样本重复 1 行）
gatk IndexFeatureFile -F <DATA_DIR>/SAMPLE_13.raw.gvcf.gz 
# ...（同上，对其余样本重复 3 行）
gatk IndexFeatureFile -F <DATA_DIR>/SAMPLE_17.raw.gvcf.gz
gatk IndexFeatureFile -F <DATA_DIR>/SAMPLE_18.raw.gvcf.gz 
# ...（同上，对其余样本重复 2 行）


gatk --java-options "-Djava.io.tmpdir=./temp -Xms4G -Xmx10G" CombineGVCFs \
-R <REF_DIR>/VS1.final.fa \
-V <DATA_DIR>/SAMPLE_01.raw.gvcf.gz \
# ...（同上，对其余样本重复 19 行）
-O <DATA_DIR>/captureGRP.combine.g.vcf.gz

gatk --java-options "-Djava.io.tmpdir=./temp -Xms4G -Xmx10G" GenotypeGVCFs \
-R <REF_DIR>/VS1.final.fa \
-V <DATA_DIR>/captureGRP.combine.g.vcf.gz \
--include-non-variant-sites \
-O <DATA_DIR>/captureGRP_includenon.raw.vcf.gz

##用4.5解决这个命令
mkdir -p <DATA_DIR>/java_tmp
chmod 777 <DATA_DIR>/java_tmp
java -Xmx10g -Djava.io.tmpdir=<DATA_DIR>/java_tmp -jar gatk-package-4.5.0.0-local.jar GenotypeGVCFs -R <REF_DIR>/VS1.final.fa -V <DATA_DIR>/GRP.combine4.g.vcf.gz --include-non-variant-sites --allow-old-rms-mapping-quality-annotation-data -O <DATA_DIR>/GRP_includenon.raw.vcf.gz


###preseq

samtools sort -@ 20 -m 4G -o bbb.mapped.maponly.sorted.bam bbb.mapped.maponly.bam
preseq c_curve -o SAMPLE_21.mapped.sort.c_cureve -B SAMPLE_21.mapped.sort.bam  -v -s 10000 -P ##没有-v就不输出内容？没-s就不输出  10000就差不多,貌似不要带p好点，毕竟是纯adna配对的可能性很小
preseq lc_extrap -B SAMPLE_21.mapped.sort.bam -v -o SAMPLE_21.mapped.sort.lc_extrap -v -s 10000 -P
ERROR:  Library expected to saturate in doubling of size, unable to extrapolate
##现在的一个问题是对不上现在的数据，如何只评估数量呢？q30不过滤只标记

preseq别忘了，不对劲搞不出来，应该是已经到了复杂度的瓶颈，另外unique数量对不上，1个原因是软件不一样，另外一个是q30的问题，他理论上来讲是要算你有多少reads，然后能拿到多少unique，所以你的初始reads还需要进行一次换算和raw的产出率。


nohup bcftools view -R target_regions.bed ACC_01.g.vcf.gz -Oz -o ACC_01target.g.vcf.gz &
# ...（同上，对其余样本重复 19 行）


gatk SortVcf -I ACC_01target.g.vcf.gz -O ACC_01target_sort.g.vcf.gz
nohup gatk SortVcf -I ACC_02target.g.vcf.gz -O ACC_02target_sort.g.vcf.gz &
# ...（同上，对其余样本重复 18 行）

gatk IndexFeatureFile -F ACC_01target_sort.g.vcf.gz
nohup gatk IndexFeatureFile -F ACC_02target_sort.g.vcf.gz &
# ...（同上，对其余样本重复 18 行）

gatk --java-options "-Djava.io.tmpdir=./temp -Xms4G -Xmx10G" CombineGVCFs \
-R <REF_DIR>/VS1.final.fa \
-V ACC_01target_sort.g.vcf.gz \
# ...（同上，对其余样本重复 19 行）
-O <DATA_DIR>/GRP.combine.g.vcf.gz


#4.5 combine
java -Xmx20g -Djava.io.tmpdir=<DATA_DIR>/java_tmp -jar gatk-package-4.5.0.0-local.jar CombineGVCFs \
-R <REF_DIR>/VS1.final.fa \
-V <DATA_DIR>/ACC_02.g.vcf.gz  \
# ...（同上，对其余样本重复 17 行）
-O <DATA_DIR>/GRP.combine_new.g.vcf.gz

nohup gatk SortVcf -I ACC_01_updatedpos.g.vcf.gz -O ACC_01_updatedpos1.g.vcf.gz &
# ...（同上，对其余样本重复 19 行）

nohup gatk IndexFeatureFile -F ACC_01_updatedpos.g.vcf.gz &
# ...（同上，对其余样本重复 7 行）
nohup gatk IndexFeatureFile -F ACC_09_updatedpos.g.vcf.gz &c
nohup gatk IndexFeatureFile -F ACC_10_updatedpos.g.vcf.gz &
# ...（同上，对其余样本重复 10 行）

bcftools view -R ../../target_pos.bed ACC_01_updated.g.vcf.gz -Oz -o ACC_01_updatedpos.g.vcf.gz  
nohup bcftools view -R ../../target_pos.bed ACC_02_updated.g.vcf.gz -Oz -o ACC_02_updatedpos.g.vcf.gz &  
# ...（同上，对其余样本重复 18 行）





java -Xmx10g -Djava.io.tmpdir=<DATA_DIR>/java_tmp -jar gatk-package-4.5.0.0-local.jar GenotypeGVCFs -R <REF_DIR>/VS1.final.fa -V <DATA_DIR>/GRP.combine19.g.vcf.gz --include-non-variant-sites --allow-old-rms-mapping-quality-annotation-data -O <DATA_DIR>/GRP_includenon.raw.vcf.gz


##换GenomicsDBImport，不然太慢了
   java -Xmx10g -Djava.io.tmpdir=<DATA_DIR>/java_tmp -jar gatk-package-4.5.0.0-local.jar GenomicsDBImport \
   --genomicsdb-workspace-path <DATA_DIR>/database \
   --batch-size 20 \
   --sample-name-map my_sample_map_corrected.txt \
   --reader-threads 30 \
   -L intervals.list \
   -R <REF_DIR>/VS1.final.fa

ln -s <DATA_DIR>/ACC_01target_sort.g.vcf.gz ACC_01target_sort.g.vcf.gz 
# ...（同上，对其余样本重复 19 行）
ln -s <DATA_DIR>/ACC_01target_sort.g.vcf.gz.tbi ACC_01target_sort.g.vcf.gz.tbi 
# ...（同上，对其余样本重复 19 行）



#!/bin/bash

# 遍历当前目录下的所有.g.vcf文件
for gvcf in *target_sort.g.vcf.gz; do
    # 从文件名中提取样品ID，这里假设样品ID就是文件名前缀
    # 例如，如果文件名是sample123.g.vcf，样品ID将是sample123
    sample_id="${gvcf%target_sort.g.vcf.gz}"
    
    # 创建一个包含新样品名的临时header文件
    echo "$sample_id" > new_sample_name.txt
    
    # 使用bcftools reheader更新样品名
    bcftools reheader -s new_sample_name.txt -o "${sample_id}_updated.g.vcf.gz" "$gvcf"
    
    # 打印更新信息
    echo "Updated sample name in $gvcf to $sample_id"
done

# 清理临时文件
rm new_sample_name.txt






##算缺失率
#!/bin/bash
# 替换为你的VCF文件名
vcf_file="captureGRP_includenon_targetpos1.raw.vcf.gz"
# 使用bcftools查询样本名称
samples=$(bcftools query -l $vcf_file)
# 使用bcftools统计总位点数
total_sites=$(zgrep -v '^#' $vcf_file | wc -l)
# 输出文件名
output_file="capGRP.sample_missing_data.txt"
# 创建或清空输出文件
> $output_file
# 遍历每个样本
for sample in $samples; do
    # 计算每个样本的缺失位点数
    missing_sites=$(bcftools view -s $sample $vcf_file | zgrep -v '^#' | grep '\./\.' | wc -l)
    # 计算缺失率
    missing_rate=$(echo "scale=4; $missing_sites / $total_sites" | bc)
    # 输出到文件
    echo "Sample $sample has $missing_sites missing sites out of $total_sites total sites, with a missing rate of $missing_rate" >> $output_file
done
echo "Output written to $output_file"

（各样本缺失率结果已删除）

merge isreal

ln -s <DATA_DIR>/SAMPLE_A.mapped.maponly.sorted.qF.sorted.cleaned.rmdup.MarkD.bam ./SAMPLE_A.mapped.maponly.sorted.qF.sorted.cleaned.rmdup.MarkD.bam
ln -s <DATA_DIR>/SAMPLE_B.mapped.maponly.sorted.qF.sorted.cleaned.rmdup.MarkD.bam ./SAMPLE_B.mapped.maponly.sorted.qF.sorted.cleaned.rmdup.MarkD.bam
ln -s <DATA_DIR>/SAMPLE_C.mapped.maponly.sorted.qF.sorted.cleaned.rmdup.MarkD.bam ./SAMPLE_C.mapped.maponly.sorted.qF.sorted.cleaned.rmdup.MarkD.bam
ln -s <DATA_DIR>/SAMPLE_D.mapped.maponly.sorted.qF.sorted.cleaned.rmdup.MarkD.bam ./SAMPLE_D.mapped.maponly.sorted.qF.sorted.cleaned.rmdup.MarkD.bam
ln -s <DATA_DIR>/SAMPLE_E.mapped.maponly.sorted.qF.sorted.cleaned.rmdup.MarkD.bam ./SAMPLE_E.mapped.maponly.sorted.qF.sorted.cleaned.rmdup.MarkD.bam
ln -s <DATA_DIR>/SAMPLE_F.mapped.maponly.sorted.qF.sorted.cleaned.rmdup.MarkD.bam ./SAMPLE_F.mapped.maponly.sorted.qF.sorted.cleaned.rmdup.MarkD.bam
ln -s <DATA_DIR>/SAMPLE_G.mapped.maponly.sorted.qF.sorted.cleaned.rmdup.MarkD.bam ./SAMPLE_G.mapped.maponly.sorted.qF.sorted.cleaned.rmdup.MarkD.bam
ln -s <DATA_DIR>/SAMPLE_H.mapped.maponly.sorted.qF.sorted.cleaned.rmdup.MarkD.bam ./SAMPLE_H.mapped.maponly.sorted.qF.sorted.cleaned.rmdup.MarkD.bam
ln -s <DATA_DIR>/SAMPLE_Acap.mapped.maponly.sorted.qF.sorted.cleaned.rmdup.MarkD.bam ./SAMPLE_Acap.mapped.maponly.sorted.qF.sorted.cleaned.rmdup.MarkD.bam
ln -s <DATA_DIR>/SAMPLE_Bcap.mapped.maponly.sorted.qF.sorted.cleaned.rmdup.MarkD.bam ./SAMPLE_Bcap.mapped.maponly.sorted.qF.sorted.cleaned.rmdup.MarkD.bam
ln -s <DATA_DIR>/SAMPLE_Ccap.mapped.maponly.sorted.qF.sorted.cleaned.rmdup.MarkD.bam ./SAMPLE_Ccap.mapped.maponly.sorted.qF.sorted.cleaned.rmdup.MarkD.bam
ln -s <DATA_DIR>/SAMPLE_Dcap.mapped.maponly.sorted.qF.sorted.cleaned.rmdup.MarkD.bam ./SAMPLE_Dcap.mapped.maponly.sorted.qF.sorted.cleaned.rmdup.MarkD.bam
ln -s <DATA_DIR>/SAMPLE_Ecap.mapped.maponly.sorted.qF.sorted.cleaned.rmdup.MarkD.bam ./SAMPLE_Ecap.mapped.maponly.sorted.qF.sorted.cleaned.rmdup.MarkD.bam
ln -s <DATA_DIR>/SAMPLE_Fcap.mapped.maponly.sorted.qF.sorted.cleaned.rmdup.MarkD.bam ./SAMPLE_Fcap.mapped.maponly.sorted.qF.sorted.cleaned.rmdup.MarkD.bam
ln -s <DATA_DIR>/SAMPLE_Gcap.mapped.maponly.sorted.qF.sorted.cleaned.rmdup.MarkD.bam ./SAMPLE_Gcap.mapped.maponly.sorted.qF.sorted.cleaned.rmdup.MarkD.bam
ln -s <DATA_DIR>/SAMPLE_Hcap.mapped.maponly.sorted.qF.sorted.cleaned.rmdup.MarkD.bam ./SAMPLE_Hcap.mapped.maponly.sorted.qF.sorted.cleaned.rmdup.MarkD.bam




C=`cat list`
for F in $C
do
echo $F >> reads_count_summary.txt
samtools merge ${F}.merged.bam ${F}.mapped.maponly.sorted.qF.sorted.cleaned.rmdup.MarkD.bam ${F}cap.mapped.maponly.sorted.qF.sorted.cleaned.rmdup.MarkD.bam
samtools view -c ${F}.mapped.maponly.sorted.qF.sorted.cleaned.rmdup.MarkD.bam >> reads_count_summary.txt
samtools view -c ${F}cap.mapped.maponly.sorted.qF.sorted.cleaned.rmdup.MarkD.bam >> reads_count_summary.txt
samtools view -c ${F}.merged.bam >> reads_count_summary.txt
wait
conda deactivate
wait
java -jar <DATA_DIR>/picard.jar CleanSam INPUT=${F}.merged.bam OUTPUT=${F}.merged.cleaned.bam
java -jar <DATA_DIR>/picard.jar MarkDuplicates INPUT=${F}.merged.cleaned.bam OUTPUT=${F}.merged.cleaned.rmdup.MarkD.bam REMOVE_DUPLICATES=TRUE AS=TRUE METRICS_FILE=${F}.merged.cleaned.rmdup.MarkD.metrics VALIDATION_STRINGENCY=SILENT 
conda activate
wait
samtools view -c ${F}.merged.cleaned.rmdup.MarkD.bam >> reads_count_summary.txt
wait
done

#整理运行r


#长度分布
C=`cat list`
for F in $C
do
samtools view ${F}cap.mapped.maponly.sorted.qF.sorted.cleaned.rmdup.MarkD.bam | awk '{print length($10)}' | sort | uniq -c > ${F}cap.length_distribution.txt
samtools view ${F}.mapped.maponly.sorted.qF.sorted.cleaned.rmdup.MarkD.bam | awk '{print length($10)}' | sort | uniq -c > ${F}.length_distribution.txt
done





##比较两个vcf差异
bcftools isec file1.vcf file2.vcf -p output_dir

##ID改成一样的
while IFS=\t read -r old_id new_info
do
  sed -i "s/$old_id/$new_info/g" 0002.id.vcf
done < id_list

 
 ##统计每一列的信息
bcftools query -f '%CHROM\t%POS\t%REF\t%ALT[\t%GT]\n' 0002.id.vcf.gz | cut -f 5 | sort | uniq -c


tabix -p vcf 0002.id.vcf.gz
tabix -p vcf 0003.id.vcf.gz

##输出基因型
bcftools query -f '%CHROM\t%POS\t%REF\t%ALT[\t%SAMPLE=%GT]\n' 0003.id.vcf.gz  > cap_genotypes.txt
```

## 比较基本的纯合杂合变化 step1
```python
import pandas as pd

# 修改这些路径以匹配你的文件位置
path_wgs = "wgs_genotypes.txt"
path_cap = "cap_genotypes.txt"

# 读取数据
df_wgs = pd.read_csv(path_wgs, sep="\t", header=None)
df_cap = pd.read_csv(path_cap, sep="\t", header=None)

# 假设前四列分别是染色体、位置、参考碱基、变异碱基，其余的是样本基因型
# 为简化处理，我们可以先将样本基因型的列转换为长格式
df_wgs_long = df_wgs.melt(id_vars=[0,1,2,3], var_name="Sample", value_name="Genotype_wgs")
df_cap_long = df_cap.melt(id_vars=[0,1,2,3], var_name="Sample", value_name="Genotype_cap")

# 合并两个数据集以便于比较
df_merged = pd.merge(df_wgs_long, df_cap_long, on=[0,1,"Sample"])

# 计算一致性
df_merged['Consistent'] = df_merged['Genotype_wgs'] == df_merged['Genotype_cap']
consistency_rate = df_merged['Consistent'].mean()
print(f"总体一致性率: {consistency_rate*100:.2f}%")

# 分析差异类型
df_merged['Discrepancy_Type'] = None
df_merged.loc[df_merged['Genotype_wgs'] != df_merged['Genotype_cap'], 'Discrepancy_Type'] = df_merged.apply(lambda x: 'Hetero_to_Homo' if '0/1' in x['Genotype_wgs'] or '1/0' in x['Genotype_wgs'] else ('Homo_to_Hetero' if '0/0' in x['Genotype_cap'] or '1/1' in x['Genotype_cap'] else 'Other'), axis=1)

discrepancy_counts = df_merged['Discrepancy_Type'].value_counts(normalize=True) * 100
print(discrepancy_counts)

```

### 全套重新统计看看 step2
```python

import pandas as pd
import numpy as np


# 根据你的文件路径调整字符串
path_to_wgs_file = 'wgs_genotypes.txt'
path_to_cap_file = 'cap_genotypes.txt'

# 尝试读取文件，并假设没有表头
df_wgs = pd.read_csv(path_to_wgs_file, sep='\t', header=None)
df_cap = pd.read_csv(path_to_cap_file, sep='\t', header=None)

# 打印前几行数据以检查它们
print(df_wgs.head())
print(df_cap.head())

# 选择一个样本列来检查基因型格式，假设它是第5列
sample_genotypes_wgs = df_wgs.iloc[:, 4]
sample_genotypes_cap = df_cap.iloc[:, 4]

# 打印出基因型数据的唯一值来检查格式
print(sample_genotypes_wgs.unique())
print(sample_genotypes_cap.unique())

# 清洗基因型数据，移除样本名前缀
for col in df_wgs.columns[4:]:
    df_wgs[col] = df_wgs[col].str.split('=').str[1]
    df_cap[col] = df_cap[col].str.split('=').str[1]

# 再次检查基因型数据的唯一值
print(df_wgs.iloc[:, 4].unique())
print(df_cap.iloc[:, 4].unique())


# 初始化差异统计字典
discrepancy_types = {
    '0/0→0/1': 0,
    '0/0→1/1': 0,
    '0/1→0/0': 0,
    '0/1→1/1': 0,
    '1/1→0/0': 0,
    '1/1→0/1': 0,
    'Consistent': 0
}

# 对每个样本遍历所有位点进行基因型比较
for col in df_wgs.columns[4:]:
    for i in range(len(df_wgs)):
        genotype_wgs = df_wgs[col].iat[i]
        genotype_cap = df_cap[col].iat[i]
        # 为了简化，我们不考虑包含'2'的基因型
        if '2' in genotype_wgs or '2' in genotype_cap:
            continue
        # 构建差异类型的key
        key = f'{genotype_wgs}→{genotype_cap}'
        # 增加差异类型的计数，或者计为一致
        if genotype_wgs == genotype_cap:
            discrepancy_types['Consistent'] += 1
        elif key in discrepancy_types:
            discrepancy_types[key] += 1
        else:
            # 如果遇到新的差异类型，可以添加到字典中
            discrepancy_types[key] = discrepancy_types.get(key, 0) + 1

# 输出差异统计结果
print(discrepancy_types)

# 计算每种差异类型的百分比和标准误差
total_discrepancies = sum(discrepancy_types.values()) - discrepancy_types['Consistent']
discrepancy_proportions = {k: (v / total_discrepancies * 100) for k, v in discrepancy_types.items() if k != 'Consistent'}
discrepancy_se = {k: np.sqrt((prop / 100 * (1 - prop / 100)) / total_discrepancies) * 100 for k, prop in discrepancy_proportions.items()}

# 打印结果
for k, v in discrepancy_proportions.items():
    print(f"{k}: {v:.2f}% (SE: {discrepancy_se[k]:.2f}%)")
```
（结果已删除）

## 输出更详细的信息 step3
```python
import pandas as pd
import numpy as np

# 根据你的文件路径调整字符串
path_to_wgs_file = 'wgs_genotypes.txt'
path_to_cap_file = 'cap_genotypes.txt'

# 尝试读取文件，并假设没有表头
df_wgs = pd.read_csv(path_to_wgs_file, sep='\t', header=None)
df_cap = pd.read_csv(path_to_cap_file, sep='\t', header=None)

# 打印前几行数据以检查它们
print(df_wgs.head())
print(df_cap.head())

# 选择一个样本列来检查基因型格式，假设它是第5列
sample_genotypes_wgs = df_wgs.iloc[:, 4]
sample_genotypes_cap = df_cap.iloc[:, 4]

# 打印出基因型数据的唯一值来检查格式
print(sample_genotypes_wgs.unique())
print(sample_genotypes_cap.unique())

# 清洗基因型数据，移除样本名前缀
for col in df_wgs.columns[4:]:
    df_wgs[col] = df_wgs[col].str.split('=').str[1]
    df_cap[col] = df_cap[col].str.split('=').str[1]

# 再次检查基因型数据的唯一值
print(df_wgs.iloc[:, 4].unique())
print(df_cap.iloc[:, 4].unique())
# 假设df_wgs和df_cap是清洗后的DataFrame，sample_columns是样本列名列表

sample_columns = df_wgs.columns[4:]  # 样本列名
# 初始化一个字典来存储统计结果
sample_stats = {}

# 遍历每个样本，计算一致性、差异性以及变异类型
for sample in sample_columns:
    consistent = 0
    discrepancies = 0
    discrepant_positions = []
    variation_stats = {'0/0→0/1': 0, '0/0→1/1': 0, '0/1→0/0': 0, '0/1→1/1': 0, '1/1→0/0': 0, '1/1→0/1': 0, 'Consistent': 0, 'Other': 0}
    
    for i in range(len(df_wgs)):
        genotype_wgs = df_wgs[sample].iat[i].split('=')[-1]
        genotype_cap = df_cap[sample].iat[i].split('=')[-1]
        
        # 判断一致性
        if genotype_wgs == genotype_cap:
            consistent += 1
            variation_stats['Consistent'] += 1
        else:
            discrepancies += 1
            discrepant_position = {'CHROM': df_wgs[0].iat[i], 'POS': df_wgs[1].iat[i], 'wgs': genotype_wgs, 'cap': genotype_cap}
            discrepant_positions.append(discrepant_position)
            
            # 记录变异类型
            change_key = f'{genotype_wgs}→{genotype_cap}'
            if change_key in variation_stats:
                variation_stats[change_key] += 1
            else:
                variation_stats['Other'] += 1
    
    # 计算百分比
    total_positions = consistent + discrepancies
    consistent_pct = (consistent / total_positions) * 100 if total_positions else 0
    discrepancies_pct = (discrepancies / total_positions) * 100 if total_positions else 0
    
    # 打印样本的一致性和差异性统计
    print(f"Sample: {sample}")
    print(f"Consistent: {consistent} ({consistent_pct:.2f}%)")
    print(f"Discrepancies: {discrepancies} ({discrepancies_pct:.2f}%)")
    print(f"Discrepant Positions (first 5): {discrepant_positions[:5]}")
    
    # 打印样本的变异类型统计
    print("Variation Stats:")
    for variation, count in variation_stats.items():
        if variation != 'Consistent':  # 已经打印了一致性信息
            print(f"{variation}: {count}")
    print('---')
```
（逐样本结果已删除）

### 版本2 详细others step4
```python
import pandas as pd
import numpy as np

# 根据你的文件路径调整字符串
path_to_wgs_file = 'wgs_genotypes.txt'
path_to_cap_file = 'cap_genotypes.txt'

# 尝试读取文件，并假设没有表头
df_wgs = pd.read_csv(path_to_wgs_file, sep='\t', header=None)
df_cap = pd.read_csv(path_to_cap_file, sep='\t', header=None)

# 打印前几行数据以检查它们
print(df_wgs.head())
print(df_cap.head())

# 选择一个样本列来检查基因型格式，假设它是第5列
sample_genotypes_wgs = df_wgs.iloc[:, 4]
sample_genotypes_cap = df_cap.iloc[:, 4]

# 打印出基因型数据的唯一值来检查格式
print(sample_genotypes_wgs.unique())
print(sample_genotypes_cap.unique())

# 清洗基因型数据，移除样本名前缀
for col in df_wgs.columns[4:]:
    df_wgs[col] = df_wgs[col].str.split('=').str[1]
    df_cap[col] = df_cap[col].str.split('=').str[1]

# 再次检查基因型数据的唯一值
print(df_wgs.iloc[:, 4].unique())
print(df_cap.iloc[:, 4].unique())
# 假设df_wgs和df_cap是清洗后的DataFrame，sample_columns是样本列名列表

# 从DataFrame中提取包含基因型信息的列名
sample_columns = df_wgs.columns[4:]  # 假设基因型信息从第5列开始

# 遍历每个样本，计算一致性、差异性以及变异类型
for sample in sample_columns:
    consistent = 0
    discrepancies = 0
    discrepant_positions = []
    variation_stats = {'0/0→0/1': 0, '0/0→1/1': 0, '0/1→0/0': 0, '0/1→1/1': 0, '1/1→0/0': 0, '1/1→0/1': 0, 'Consistent': 0, 'Other': 0}
    
    for i in range(len(df_wgs)):
        genotype_wgs = df_wgs[sample].iat[i].split('=')[-1]
        genotype_cap = df_cap[sample].iat[i].split('=')[-1]
        
        if genotype_wgs == genotype_cap:
            consistent += 1
            variation_stats['Consistent'] += 1
        else:
            discrepancies += 1
            discrepant_position = {'CHROM': df_wgs[0].iat[i], 'POS': df_wgs[1].iat[i], 'wgs': genotype_wgs, 'cap': genotype_cap}
            discrepant_positions.append(discrepant_position)
            change_key = f'{genotype_wgs}→{genotype_cap}'
            variation_stats[change_key] = variation_stats.get(change_key, 0) + 1
    
    total_positions = consistent + discrepancies
    consistent_pct = (consistent / total_positions * 100) if total_positions else 0
    discrepancies_pct = (discrepancies / total_positions * 100) if total_positions else 0
    
    print(f"Sample: {sample}")
    print(f"Consistent: {consistent} ({consistent_pct:.2f}%)")
    print(f"Discrepancies: {discrepancies} ({discrepancies_pct:.2f}%)")
    print("Variation Stats:")
    for variation, count in variation_stats.items():
        print(f"  {variation}: {count}")
    print(f"Discrepant Positions (first 5): {discrepant_positions[:5]}")
    print('---')


```
（逐样本结果已删除）
