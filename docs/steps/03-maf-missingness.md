# 3. Filter MAF and missingness

## Input

- Recorded in the local notebook at lines 251–296, under this step.
- A loop writes one cluster script per chromosome.
- Input named in the filter line: `.../Grape.${i}.pass_snp.vcf.gz`.
- Lines 297–298 are a later filter the notes say was already done. The file named later is `Grape.0_05maf_0_4mis_pass_snps_filtered.vcf.gz`.

## Do

```bash
vcftools --gzvcf .../Grape.${i}.pass_snp.vcf.gz --max-missing 0.5 --maf 0.01 --min-alleles 2 --max-alleles 2 --recode --stdout | gzip
gatk MergeVcfs
```

## Get

- Output name in the filter line: `Grape.${i}.0_01maf_0_5mis_pass_snps_filtered.vcf.gz`.
- The following merge script's `-I` names use `0_1maf` instead of `0_01maf`. The notes do not explain the rename.
- Merge is a pasted cluster `gatk MergeVcfs` of chromosomes 1–19 to `Grape.0_1maf_0_5mis_pass_snps_filtered.vcf.gz`.
- No `vcftools` line for `--maf 0.05` or `--max-missing 0.4` appears in the later section. The notes say that filter was already done.
