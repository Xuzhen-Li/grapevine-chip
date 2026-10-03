# Design steps

Source: local notebook `00_array/##芯片位点处理全流程.md` (1836 lines). Line numbers below are that file. Commands were copied out of a working notebook. A block that starts with `#!/bin/bash` and `#SBATCH` is a pasted cluster job, not a command this repository runs or supports. Cluster paths under `/public/gxyy/...` are left as names of what the notes point at; they are not reproduced here as a recipe.

Sequencing results stay off GitHub. This file does not include VCFs, BAMs, or probe tables.

## 1. Look at where reads and sites fall on the annotation

Notebook lines 3–36, section `古生物分布特征`.

`samtools depth` and `sambamba depth -t 10 -w 500` are written as ways to see base or window depth. `bedtools intersect` against `VS1.final.gff3` is written to count how captured sites fall on features. One pasted count, from `final_capture_ld05maf05mis04dp10_2kb_gff3_10kpanel_maf.bed` against `annotation.gff3`, is:

| feature | count pasted in the notes |
| --- | --- |
| `.` | 45212 |
| CDS | 50292 |
| exon | 60112 |
| five_prime_UTR | 4100 |
| gene | 116589 |
| mRNA | 125290 |
| TandemRepeat | 9773 |
| TEprotein | 1113 |
| three_prime_UTR | 5720 |
| Transposon | 112874 |

The next line says this still drops some regions. These are overlap counts in the notes, not a frozen panel size.

Lines 44–164 are pasted SLURM jobs that turn BAM depth or panel positions into CMplot density CSVs (`samtools depth`, drop `HiC_scaffold`, `qualimap bamqc`). They are sample-coverage pictures, not site selection.

## 2. Annotate SNP function

Lines 167–222, `SNP信息注释`.

1. `gff3ToGenePred` on `VS1.final.gff3`, then `retrieve_seq_from_fasta.pl` on `VS1.final.fa`.
2. `python vcf2annovar.py` to a five-column ANNOVAR file (chromosome, start, end, ref, alt). The converter is not in the local `00_array` folder.
3. `annotate_variation.pl --buildver VS1 --geneanno`.

A later pasted SLURM job (lines 198–209) subsets `Grape.pass_biallel.vcf.gz` with `--positions` on `final_capture_ld05maf05mis04dp10_2kb_gff3_10kpanel_maf.txt` before the same annotation. `uniq -c` on `Grape.pass.variant_function` is pasted as: downstream 11664, exonic 47999, exonic;splicing 1, intergenic 95593, intronic 58886, splicing 85, upstream 12335, upstream;downstream 1305, UTR3 4891, UTR5 3501.

PROVEAN is described for missense sites. The notes say a score less than -2.5 is deleterious and other scores are neutral, and that the old NR, PSI-BLAST, CD-HIT, and blastdbcmd versions have to match PROVEAN (CD-HIT v4.0 is the version named). No local PROVEAN script is in `00_array`.

## 3. Filter MAF and missingness

Lines 251–296, `过滤MAF01，MIS05`.

A loop writes one SLURM script per chromosome. The only filter line is:

`vcftools --gzvcf .../Grape.${i}.pass_snp.vcf.gz --max-missing 0.5 --maf 0.01 --min-alleles 2 --max-alleles 2 --recode --stdout | gzip`

Output name in that line: `Grape.${i}.0_01maf_0_5mis_pass_snps_filtered.vcf.gz`. The following merge script's `-I` names use `0_1maf` instead of `0_01maf`. The notes do not explain the rename. Merge is a pasted SLURM `gatk MergeVcfs` of chromosomes 1–19 to `Grape.0_1maf_0_5mis_pass_snps_filtered.vcf.gz`.

Lines 297–298, `过滤MAF005MIS04`: "之前已经有了" (already done). The file named later is `Grape.0_05maf_0_4mis_pass_snps_filtered.vcf.gz`. No `vcftools` line for `--maf 0.05` / `--max-missing 0.4` appears in this section.

## 4. LD prune

Lines 300–310, `过滤LD（MAF01MIS05）`.

Not wrapped as SBATCH in the notebook (plain shell lines):

- `plink --allow-extra-chr --recode --chr-set 19 --gzvcf Grape.0_1maf_0_5mis_pass_snps_filtered.vcf.gz --make-bed`
- rewrite the map ID as `chrom_pos`
- `plink --file ... --indep-pairwise 50 5 0.5`, and the same with `0.3` and `0.1`
- `perl get_keep.pl` on each `.prune.in` to write `core.05mis01maf.ld01.snp.vcf.gz`, `ld03`, and `ld05`

`get_keep.pl` is not in the local `00_array` folder.

Lines 312–323, `过滤LD（MAF005MIS04）`. A pasted SLURM script runs only `plink --file s1_vcf --indep-pairwise 50 5 0.1` and `get_keep.pl` into `core.005maf04mis.ld0.1.snp.vcf.gz` from `Grape.0_05maf_0_4mis_pass_snps_filtered.vcf.gz`. The note says the other cutoffs were already there and this adds 0.1.

## 5. Mean depth

Lines 325–338, `限制每个snp上的reads数目`.

Prose: "10条" and `--min-meanDP 10`. The pasted SLURM script runs `vcftools --min-meanDP 10` on:

- `core.0.4mis0.05maf.ld0.3.snp.vcf.gz`
- `core.0.4mis0.05maf.ld0.1.snp.vcf.gz`
- `core.0.4mis0.05maf.ld0.4.snp.vcf.gz`

and writes the same names with `_dp10`. How the r² 0.4 file was produced is not pasted (see step 4).

## 6. Recompute MAF and make a BED

Lines 342–388, `maf计算`.

Pasted SLURM: `vcftools --freq`, `--freq2`, `--counts`, `--counts2` on `core.0.4mis0.05maf.ld0.3.snp_dp10.vcf.gz`. The notes say plink `--freq` was not usable. The BED used downstream is:

`awk '{if($5<$6)print $1"\t"$2"\t"$2+1"\t"$5; else print $1"\t"$2"\t"$2+1"\t"$6}' ld3_freq2.frq > ld03_maf2bed.bed`

So the score is the smaller of the two `--freq2` allele counts, on a 1 bp interval. A second awk writes sites without the score (`ld03_maf2sites.bed`).

Lines 573–591 recompute `--freq2` for r² 0.1, 0.4, 0.5, 0.7, `ldtotal`, and several `panel.*` VCFs. That block is also a pasted SLURM script (`frq2_all`). One input named there is `core.0.4mis0.05maf.ld0.7.snp_dp10.vcf.gz`; no prune command for 0.7 was pasted.

## 7. Split named populations

Lines 390–406.

Groups written in the notes: `CG1-6`, `WWE12`, `WEE12`. A loop over `*.info` files writes SLURM scripts that `vcftools --keep` the MAF 0.05 / missingness 0.4 VCF. The notebook does not define the groups.

## 8. One highest-MAF site per 2 kb window

Lines 411–440 (a fenced bash block the notes mark `###final` for the window pick) and lines 595–627 (`##method 2`, a pasted SLURM script).

Window file:

`bedtools makewindows -g VS1.final.fa.2col.bed -w 2000 > VS1.window.bed`

Then, for each LD set: intersect window BED with the MAF BED, `bedtools groupby -g 1,2,3 -c 5 -o max`, intersect back, and keep rows where the site score equals the window max (`awk '{if($5==$9) ...}'`). Positions go to `ld{01,03,04,05}maf05mis04dp10_2kb.maf_array_pos.txt`. `vcftools --positions` extracts a VCF from the matching `core.0.4mis0.05maf.ld0.*.snp_dp10.vcf.gz`.

The notes before the working version say a `sort` by score did not pick one site per window (row counts jumped between about 18万 and 140万 in the note text) and that `groupby -full` kept the wrong row. Those attempts are failed drafts in the same section, not a second method.

Lines 814–830 (`##method 7`, pasted SLURM, `#2kb`) repeat the 2 kb max pick on `core.0.4mis0.05maf.snp_dp10.vcf.gz` (no LD in the filename). The freq2 awk in that script reads `total_ld_freq2`, not `total_ld_freq2.frq`.

## 9. Same pick on exon, gene, and CDS

Lines 445–491 and 631–659 (exon, `##method 4`, pasted SLURM). Lines 689–693 build the BEDs. Lines 697–718 (gene, `##method 5`, pasted SLURM; the rest of the script matches the exon pattern through `vcftools --positions`). CDS is `##method 6` (heading at line 756) and the same intersect / groupby / max pattern; method 7 lines 831–839 paste the CDS and exon half of that pattern on the unpruned set.

Exon BED:

`awk -v OFS="\t" '{if($3=="exon") print $0}' VS1.final.gff3`

then chromosome, start, end, `sort|uniq`. Gene and CDS use `$3=="gene"` and `$3=="CDS"`.

The notes (lines 454–491) say exon counts did not match expectations because of alternative splicing: one site falls in more than one feature, so dedup has to start from the first intersect. They also say the assembly is Hi-C named, the GFF is numeric, and the freq file may be chromosomes only. A pasted `wc -l` (lines 662–685) records intermediate file lengths, including `VS1.final.exon.bed` 171237 lines and `ld05maf05mis04dp10_exon.maf_array_pos.txt` 51217 lines. Those are file lengths in the notes, not a released panel size.

## 10. Merge functional positions

Lines 493–494 and 898–905.

`cat` of CDS, exon, and gene `*.maf_array_pos.txt`, then `sort|uniq`, for the unpruned set and for r² 0.5, 0.3, 0.1, and 0.4 (`ld05_maf05mis04dp10_gff3_final_uniq.txt` and the ld03, ld01, ld04 twins).

## 11. Sites the notes add but do not script

- Lines 498–499, `增加10k的部分`: "回贴结果已有". No steps.
- Lines 508–510, `增加育种位点`: per-population MAF, "至少有一半的群体大于0.2（0.5*0.2？）", typed sites taken from GWAS. No command.
- Lines 512–513, `增加特有位点`: MAF = 0 inside a population and very small in the others. No command.
- Lines 515–517, `去重`: sketch `cat file1 file2 file3.... > final_merge |sort | uniq`. The redirect is written that way in the notes; it is not a finished command.

## 12. Flank sequence

- Line 41, `利用prel提取flank50`: heading only.
- Lines 521–542: `vcftools --freq2` again, site BED, then `awk 'NR==1 {next}{print $1"\t"$2-25"\t"$2+24}'` and a commented `bedtools flank -i ld03_maf2sites.bed -g VS1.final.fa.2col.bed -l 25 -r 24`. Groupby on the 25/24 windows is then rejected in the notes: overlapping blocks, and a 25 bp window "必然没有意义" if adjacent windows touch. The 2 kb window (step 8) is what the notes say replaced this.
- Local `00_array/lifeover/megablast.sh` (25 lines, itself wrapped in a markdown fence) sets `FLANK=100` for chromosome 1 position 3055017, `samtools faidx` on `VS1.final.fa`, and `blastn -task megablast` against `v4_genome_ref.fasta`. One alignment row is pasted under the command. This is a single-site coordinate check, not the panel flank step. `lifeover/make_chain_file.sh` is a UCSC same-species liftover setup whose download example is *Glycine max*, not the grapevine panel.

## 13. What the notes call the capture freeze

Lines 552–554: Illumina scoring "放在最后一步", "准备三个文件格式". No formats and no command.

Lines 907–909, `##final` / `#1 capture`:

`cat ld05_maf05mis04dp10_gff3_final_uniq.txt ld05maf05mis04dp10_2kb.maf_array_pos.txt panel_raw.vcf.gz | sort | uniq | wc -l`

The third input is a VCF filename. The notes do not record the `wc -l` result. Do not treat this line as a cleaned site list.

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

## Local files checked and not used as steps

| path under `00_array` | what it is |
| --- | --- |
| `intervalpos&region.py` | Interval tree of `wgs.pos` against `fianl_pos.txt`. One-off overlap of local position files. |
| `matched_intervals.py` | Matches `dedup_overlaps_region.txt` to probe-cover rows in `WGStest.csv`. One-off. |
| `stat_vcf_from_3527/maf_distribution.py` | Histogram of a chip MAF BED. |
| `stat_vcf_from_3527/pos_interval_stat.py` | Distance between adjacent sites, plotted. |
| `stat_vcf_from_3527/stat_rate.py` | Boxplot of het and missing rates. |

Those are checks or plots on data already in hand. They are not steps of the design path above.
