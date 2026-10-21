!/bin/bash
# checkbam.sh  用法：bash checkbam.sh in.bam
set -e
bam=$1
echo "count FLAG meaning" > flag_stat.txt

# 1. 统计每种 FLAG
samtools view -F 0 "$bam" | awk '{print $2}' | sort -n | uniq -c | sort -nr |
while read cnt flag; do
  # 2. Bash 逐位解码
  meaning=""
  (( flag & 1    )) && meaning="${meaning}paired,"
  (( flag & 2    )) && meaning="${meaning}proper_pair,"
  (( flag & 4    )) && meaning="${meaning}unmapped,"
  (( flag & 8    )) && meaning="${meaning}mate_unmapped,"
  (( flag & 16   )) && meaning="${meaning}reverse,"
  (( flag & 32   )) && meaning="${meaning}mate_reverse,"
  (( flag & 64   )) && meaning="${meaning}first_in_pair,"
  (( flag & 128  )) && meaning="${meaning}second_in_pair,"
  (( flag & 256  )) && meaning="${meaning}secondary,"
  (( flag & 512  )) && meaning="${meaning}qc_fail,"
  (( flag & 1024 )) && meaning="${meaning}duplicate,"
  (( flag & 2048 )) && meaning="${meaning}supplementary,"
  meaning=${meaning%,}   # 去掉末尾逗号
  printf "%s %s %s\n" "$cnt" "$flag" "$meaning"
done >> flag_stat.txt