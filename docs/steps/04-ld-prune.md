## 4. LD prune

Lines 300–310, `过滤LD（MAF01MIS05）`.

Not wrapped as SBATCH in the notebook (plain shell lines):

- `plink --allow-extra-chr --recode --chr-set 19 --gzvcf Grape.0_1maf_0_5mis_pass_snps_filtered.vcf.gz --make-bed`
- rewrite the map ID as `chrom_pos`
- `plink --file ... --indep-pairwise 50 5 0.5`, and the same with `0.3` and `0.1`
- `perl get_keep.pl` on each `.prune.in` to write `core.05mis01maf.ld01.snp.vcf.gz`, `ld03`, and `ld05`

`get_keep.pl` is not in the local `00_array` folder.

Lines 312–323, `过滤LD（MAF005MIS04）`. A pasted SLURM script runs only `plink --file s1_vcf --indep-pairwise 50 5 0.1` and `get_keep.pl` into `core.005maf04mis.ld0.1.snp.vcf.gz` from `Grape.0_05maf_0_4mis_pass_snps_filtered.vcf.gz`. The note says the other cutoffs were already there and this adds 0.1.

Back to [the step list](../steps.md).
