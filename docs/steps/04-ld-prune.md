# 4. LD prune

## Input

- Recorded in the local notebook at lines 300–310 for the MAF 0.01 and missingness 0.5 VCF. Those lines are plain shell, not wrapped as SBATCH.
- `Grape.0_1maf_0_5mis_pass_snps_filtered.vcf.gz`.
- Lines 312–323 are the MAF 0.05 and missingness 0.4 prune. A pasted cluster script starts from `Grape.0_05maf_0_4mis_pass_snps_filtered.vcf.gz`.
- `get_keep.pl` is not in the local `00_array` folder.
- The notes say to rewrite the map ID as `chrom_pos`. No command for that rewrite was pasted.

## Do

```bash
plink --allow-extra-chr --recode --chr-set 19 --gzvcf Grape.0_1maf_0_5mis_pass_snps_filtered.vcf.gz --make-bed
plink --file ... --indep-pairwise 50 5 0.5
plink --file ... --indep-pairwise 50 5 0.3
plink --file ... --indep-pairwise 50 5 0.1
perl get_keep.pl
plink --file s1_vcf --indep-pairwise 50 5 0.1
```

## Get

- `perl get_keep.pl` on each `.prune.in` writes `core.05mis01maf.ld01.snp.vcf.gz`, `ld03`, and `ld05`.
- The second pasted script runs only `plink --file s1_vcf --indep-pairwise 50 5 0.1` and `get_keep.pl` into `core.005maf04mis.ld0.1.snp.vcf.gz`.
- The note says the other cutoffs were already there and this adds 0.1.
