## 5. Mean depth

Lines 325–338, `限制每个snp上的reads数目`.

Prose: "10条" and `--min-meanDP 10`. The pasted SLURM script runs `vcftools --min-meanDP 10` on:

- `core.0.4mis0.05maf.ld0.3.snp.vcf.gz`
- `core.0.4mis0.05maf.ld0.1.snp.vcf.gz`
- `core.0.4mis0.05maf.ld0.4.snp.vcf.gz`

and writes the same names with `_dp10`. How the r² 0.4 file was produced is not pasted (see step 4).

Back to [the step list](../steps.md).
