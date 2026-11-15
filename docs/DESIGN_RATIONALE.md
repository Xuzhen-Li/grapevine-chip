# Why the panel is built this way

This page explains the design logic of the grapevine capture panel. Every
point comes from the step files in [steps/](steps/) and the notes in
[../notes/](../notes/). Where the notes give a reason, it is quoted as
"the notes say". Where the reason is only implied by what the commands
do, it is marked "reading of the commands". Where the notes give no
reason, that is said too.

## The idea in one paragraph

Start from whole-genome SNP calls on a grapevine collection (reference
`VS1.final.fa`, 19 chromosomes). Keep clean biallelic SNPs that are common
enough and well covered. Thin them by linkage disequilibrium, so neighbours
that carry the same information are not all kept. Then place sites evenly:
one site, the one with the highest minor allele frequency, in each 2 kb
window. Do the same pick inside exons, genes, and CDS so genic regions are
covered on purpose, merge those lists, and add planned special classes
(breeding sites, population-private sites). The union is the capture list.
After a chip is made, compare its genotypes with the whole-genome calls
on the same samples.

## Step by step

### 1. Start set: whole-genome SNPs on VS1

- Input: per-chromosome `Grape.${i}.pass_snp.vcf.gz` ([step 3](steps/03-maf-missingness.md)).
- Annotation: `VS1.final.gff3`, used for overlap counts and later for the genic picks ([step 1](steps/01-annotation-overlap.md), [step 2](steps/02-snp-function.md)).

### 2. Biallelic, MAF, and missingness filters

- First pass: `--max-missing 0.5 --maf 0.01 --min-alleles 2 --max-alleles 2` per chromosome, then merged ([step 3](steps/03-maf-missingness.md)).
- The file names used later mark a stricter set, MAF 0.05 and missingness 0.4 (`Grape.0_05maf_0_4mis_pass_snps_filtered.vcf.gz`). The notes say that filter "was already done"; the command for it was not pasted.
- Reading of the commands: biallelic sites are what a two-allele assay can score; a minimum MAF drops sites that would be monomorphic in most samples. The notes do not state these reasons in words.

### 3. LD pruning: the knob for panel size

- `plink --indep-pairwise 50 5 <r2>` with r² 0.1, 0.3, 0.5 on the loose set, and 0.1 on the strict set; file names also show 0.4 and 0.7 sets ([step 4](steps/04-ld-prune.md), [step 6](steps/06-maf-bed.md)).
- Reading of the commands: each r² cutoff gives a different number of sites, and every later step was run for several cutoffs side by side (ld01, ld03, ld04, ld05). Choosing the cutoff is how the final site count is set. The notes do not record which count was the target.

### 4. Mean depth at least 10

- `vcftools --min-meanDP 10` on the pruned sets ([step 5](steps/05-mean-depth.md)). The notes say 10 reads.
- Reading of the commands: sites with low resequencing depth have less reliable genotypes, so they are poor candidates for the panel.

### 5. Score each site by minor allele frequency

- `vcftools --freq2`, then the smaller of the two allele frequencies is written as the BED score, on a 1 bp interval (`ld03_maf2bed.bed`) ([step 6](steps/06-maf-bed.md)).
- The notes say plink `--freq` was not usable for this.

### 6. One site per 2 kb window, highest MAF wins

- `bedtools makewindows -w 2000`, intersect with the MAF BED, `groupby ... -o max`, keep the site whose score equals the window maximum ([step 8](steps/08-window-2kb.md)).
- This is the spacing rule of the panel. Reading of the commands: it spreads sites along every chromosome and, inside each window, keeps the most polymorphic one.
- The notes record two failed tries before this worked: sorting by score did not give one site per window, and `groupby -full` kept the wrong row.
- An earlier idea, 25/24 bp windows around each site, was dropped. The notes say the blocks overlapped and that a 25 bp window means nothing when windows touch; the 2 kb window replaced it ([step 12](steps/12-flank.md)).

### 7. The same pick inside exons, genes, and CDS

- The window pick is repeated on features taken from `VS1.final.gff3`: exon, gene, and CDS ([step 9](steps/09-exon-gene-cds.md)), then merged with `sort | uniq` ([step 10](steps/10-merge-functional.md)).
- Reading of the commands: this makes sure genic sequence is covered on purpose, not only by chance from the genome-wide windows.
- The notes warn that one site can fall in several features because of alternative splicing, so duplicates have to be removed from the first intersect onward.
- SNP effects were also annotated with ANNOVAR (`--buildver VS1`), and PROVEAN was described for missense sites, with scores below -2.5 called deleterious ([step 2](steps/02-snp-function.md)). The notes do not show these labels being used to select sites.

### 8. Special site classes (planned, not scripted)

From [step 11](steps/11-extra-site-classes.md):

- Sites pasted back from an earlier 10k set.
- Breeding sites: per-population MAF, at least half of the groups above 0.2, plus sites from GWAS.
- Private sites: MAF 0 inside one population and very small in the others.

No command or output file was recorded for any of these. They are design intentions only.

### 9. Probe flanks and coordinate checks

- A 50 bp flank extraction is a heading only. One site was checked with `blastn -task megablast` against `v4_genome_ref.fasta` ([step 12](steps/12-flank.md)).
- This is a single-site coordinate check. A full flank and probe-design step is not in the notes.

### 10. Freeze

- The capture list is the union of the merged genic list, the 2 kb list, and `panel_raw.vcf.gz` ([step 13](steps/13-freeze.md)).
- The notes put vendor (Illumina) scoring as the last step and say three file formats are needed. No formats or command were written down. The final count was not recorded.

## Checking a panel after it is made

[../notes/stat_array.md](../notes/stat_array.md) and `scripts/stat_italy/` hold the checks used on capture data:

- Genotype agreement between capture and whole-genome calls on the same samples, split into change types such as 0/1 to 0/0 (`scripts/stat_italy/hete2homo.py`; synthetic example in `scripts/stat_italy/example_synthetic/`). The script compares the two files row by row, so they must hold the same sites in the same order and the same samples in the same columns; it now stops if they do not (the check compares CHROM, POS, REF and ALT).
- Per-sample missing rate with `bcftools`, and library complexity with `preseq c_curve`.
- Mapped-rate change before and after capture, and before and after PCR (`group4_capeff.py`, `pcr_bias/mappedrate_fold.py`, `dna_probe/group2_map.py`).
- Site-level summaries: MAF distribution, distance between adjacent sites, het and missing rate (`scripts/stat_vcf/`, `scripts/stat_array/`).

## What is missing

- The command for the MAF 0.05 / missingness 0.4 filter, the r² 0.4 and 0.7 prunes, and `get_keep.pl`.
- Population definitions for the per-group split ([step 7](steps/07-population-split.md)).
- Any script for breeding, private, or GWAS sites.
- Probe design, vendor scoring, and the final site count.
- A separate SR4R-style branch (minimal markers, Beagle, indels) was started and not finished ([step 14](steps/14-sr4r-branch.md)).
