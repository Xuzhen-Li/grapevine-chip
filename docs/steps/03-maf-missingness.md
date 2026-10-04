## 3. Filter MAF and missingness

Lines 251–296, `过滤MAF01，MIS05`.

A loop writes one SLURM script per chromosome. The only filter line is:

`vcftools --gzvcf .../Grape.${i}.pass_snp.vcf.gz --max-missing 0.5 --maf 0.01 --min-alleles 2 --max-alleles 2 --recode --stdout | gzip`

Output name in that line: `Grape.${i}.0_01maf_0_5mis_pass_snps_filtered.vcf.gz`. The following merge script's `-I` names use `0_1maf` instead of `0_01maf`. The notes do not explain the rename. Merge is a pasted SLURM `gatk MergeVcfs` of chromosomes 1–19 to `Grape.0_1maf_0_5mis_pass_snps_filtered.vcf.gz`.

Lines 297–298, `过滤MAF005MIS04`: "之前已经有了" (already done). The file named later is `Grape.0_05maf_0_4mis_pass_snps_filtered.vcf.gz`. No `vcftools` line for `--maf 0.05` / `--max-missing 0.4` appears in this section.

Back to [the step list](../steps.md).
