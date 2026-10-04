# 6. Recompute MAF and make a BED

## Input

- Recorded in the local notebook at lines 342–388, under this step.
- Pasted cluster job on `core.0.4mis0.05maf.ld0.3.snp_dp10.vcf.gz`.
- Lines 573–591 recompute `--freq2` for r² 0.1, 0.4, 0.5, and 0.7, for `ldtotal`, and for several `panel.*` VCFs. That block is also a pasted cluster script (`frq2_all`).
- One input named there is `core.0.4mis0.05maf.ld0.7.snp_dp10.vcf.gz`. No prune command for 0.7 was pasted.

## Do

```bash
vcftools --freq
vcftools --freq2
vcftools --counts
vcftools --counts2
awk '{if($5<$6)print $1"\t"$2"\t"$2+1"\t"$5; else print $1"\t"$2"\t"$2+1"\t"$6}' ld3_freq2.frq > ld03_maf2bed.bed
```

## Get

- The notes say plink `--freq` was not usable.
- The BED used downstream is `ld03_maf2bed.bed`. The score is the smaller of the two `--freq2` allele counts, on a 1 bp interval.
- A second awk writes sites without the score (`ld03_maf2sites.bed`). That second awk body was not pasted.
