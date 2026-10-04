# 14. SR4R-style branch (separate, unfinished)

## Input

- Lines 912–944 list SR4R downloads: PCA, structure, IBS, ROH, LD, pi, Tajima's D, Fst, hapmap tools, `1.3.extractSNPflankSeq`, imputation, minimal-marker match, annotation and genotype tarballs, and indels. That is a reference the notes downloaded, not a grapevine result.
- Lines 948–967, `#0.raw`: biallelic filter on `Grape.${i}.pass_snp.vcf.gz`, pasted as per-chromosome cluster `vcftools`.
- Lines 968–987: prose says missingness under 20% of individuals, then missingness under 20% and allele frequency under 0.005, and that missingness should be applied first. The commands actually pasted at lines 1081–1087 are different.
- Lines 1088–1134: split by chromosome, Beagle `beagle.12Jul19.0df.jar`.
- A local copy of the Python tool is `00_array/minimal_marker/minimial.py` (the first lines match the dependency check). It is an external marker-minimization tool, not pasted into this repo.
- Lines 1651–1800 are an indel side branch. Pasted cluster jobs.
- Lines 1802–1829: breeding sites according to maker; fixed sites as a union with another person's lists; table versus wine; cultivar versus wild; a loop that prints columns from `Grape.CEU.${i}1.TajimaD.gene.kegg.txt` for groups A, B, C, D, F, and G. Barcode check: randomly choose 100 individuals from gVCFs. Machine learning is a heading only (line 1829). No finished commands for that last block.

## Do

```bash
vcftools --min-alleles 2 --max-alleles 2
MergeVcfs
plink --mind 0.2
plink --geno 0.1
plink --maf 0.05
plink --export vcf --out indv02mis0.1maf005_bi_snp
beagle.12Jul19.0df.jar
minimalmarkers
00_array/minimal_marker/minimial.py
SelectVariants -select-type INDEL
```

## Get

- Lines 1039–1067 merge the per-chromosome biallelic VCFs with a pasted `MergeVcfs` to `Grape.pass_biallel.vcf.gz`.
- The pasted plink output name says `maf005`. The flag in the same block is `--maf 0.05`.
- The notes also say per-chromosome plink conversion was buggy and that plink cannot feed Beagle because there is no cM map.
- The notes paste `OutOfMemoryError: GC overhead limit exceeded` and say chromosome 18 kept failing.
- Later minimal-marker runs (`minimalmarkers`, then a Python script the notes pin at Python >= 3.6, numpy >= 1.19.0, numba >= 0.50.0) are pasted cluster jobs. The notes say the jobs blew temporary files when the sample count was large, and that VCF input failed until a genotype matrix was built from `vcftools` `.012` output.
- The indel branch uses `SelectVariants -select-type INDEL`, then the same mind, geno, and maf pattern and minimal markers.
- The breeding-site, fixed-site, table-versus-wine, cultivar-versus-wild, Tajima column, barcode, and machine-learning notes have no finished command. No output of those notes was recorded.
