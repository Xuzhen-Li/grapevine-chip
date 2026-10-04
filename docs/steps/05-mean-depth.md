# 5. Mean depth

## Input

- Recorded in the local notebook at lines 325–338, under this step.
- The notes say 10 reads, and the pasted flag is `--min-meanDP 10`.
- The pasted cluster script runs on `core.0.4mis0.05maf.ld0.3.snp.vcf.gz`, `core.0.4mis0.05maf.ld0.1.snp.vcf.gz`, and `core.0.4mis0.05maf.ld0.4.snp.vcf.gz`.

## Do

```bash
vcftools --min-meanDP 10
```

## Get

- The same three names with `_dp10` appended.
- How the r² 0.4 file was produced is not pasted (see step 4).
