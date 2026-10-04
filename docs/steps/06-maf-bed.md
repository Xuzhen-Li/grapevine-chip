## 6. Recompute MAF and make a BED

Lines 342–388, `maf计算`.

Pasted SLURM: `vcftools --freq`, `--freq2`, `--counts`, `--counts2` on `core.0.4mis0.05maf.ld0.3.snp_dp10.vcf.gz`. The notes say plink `--freq` was not usable. The BED used downstream is:

`awk '{if($5<$6)print $1"\t"$2"\t"$2+1"\t"$5; else print $1"\t"$2"\t"$2+1"\t"$6}' ld3_freq2.frq > ld03_maf2bed.bed`

So the score is the smaller of the two `--freq2` allele counts, on a 1 bp interval. A second awk writes sites without the score (`ld03_maf2sites.bed`).

Lines 573–591 recompute `--freq2` for r² 0.1, 0.4, 0.5, 0.7, `ldtotal`, and several `panel.*` VCFs. That block is also a pasted SLURM script (`frq2_all`). One input named there is `core.0.4mis0.05maf.ld0.7.snp_dp10.vcf.gz`; no prune command for 0.7 was pasted.

Back to [the step list](../steps.md).
