## 14. SR4R-style branch (separate, unfinished)

Lines 912–944 list SR4R downloads (PCA, structure, IBS, ROH, LD, pi, Tajima's D, Fst, hapmap tools, `1.3.extractSNPflankSeq`, imputation, minimal-marker match, annotation and genotype tarballs, indels). That is a reference the notes downloaded, not a grapevine result.

Lines 948–967, `#0.raw`: biallelic filter, pasted as per-chromosome SLURM `vcftools --min-alleles 2 --max-alleles 2` on `Grape.${i}.pass_snp.vcf.gz`. Lines 1039–1067 merge those with a pasted `MergeVcfs` to `Grape.pass_biallel.vcf.gz`.

Lines 968–987: prose says missingness under 20% of individuals, then missingness under 20% and allele frequency under 0.005, and that missingness should be applied first. The commands actually pasted at lines 1081–1087 are different:

- `plink --mind 0.2`
- `plink --geno 0.1`
- `plink --maf 0.05`
- `--export vcf --out indv02mis0.1maf005_bi_snp`

The output name says `maf005`. The flag in the same block is `--maf 0.05`. The notes also say per-chromosome plink conversion was buggy and that plink cannot feed Beagle because there is no cM map.

Lines 1088–1134: split by chromosome, Beagle `beagle.12Jul19.0df.jar`. The notes paste `OutOfMemoryError: GC overhead limit exceeded` and say chromosome 18 kept failing. Later minimal-marker runs (perl `minimalmarkers`, then a Python script the notes pin at `Python >= 3.6`, `numpy >= 1.19.0`, `numba >= 0.50.0`) are pasted SLURM. The notes say the jobs blew temporary files when the sample count was large, and that VCF input failed until a genotype matrix was built from `vcftools` `.012` output. A local copy of that Python tool is `00_array/minimal_marker/minimial.py` (first lines match that dependency check). It is an external marker-minimization tool, not pasted into this repo.

Lines 1651–1800 are an indel side branch (`SelectVariants -select-type INDEL`, then the same mind / geno / maf pattern and minimal markers). Pasted SLURM.

Lines 1802–1829: breeding sites "根据maker"; fixed sites as a union with another person's lists; table versus wine; cultivar versus wild; a loop that prints columns from `Grape.CEU.${i}1.TajimaD.gene.kegg.txt` for groups A, B, C, D, F, G. Barcode check: "随机选100个个体" from gVCFs. Machine learning: a heading only (line 1829). No finished commands.

Back to [the step list](../steps.md).
