# Why the panel is built this way

This page explains the design rationale behind the grapevine capture panel.
Every point comes from the step files in [steps/](steps/) and the notes in
[../notes/](../notes/). Where the notes provide a reason, it is cited as
"the notes say". Where the reason is inferred from what the commands do, it
is marked "reading of the commands". Where the notes give no reason, that is
noted as well.

## The idea in one paragraph

Start from whole-genome SNP calls across a grapevine collection (reference
`VS1.final.fa`, 19 chromosomes). Retain clean biallelic SNPs that are
sufficiently common and well covered. Thin them by linkage disequilibrium so
neighboring variants carrying redundant information are not all kept. Next,
space sites evenly: keep one site—the one with the highest minor allele
frequency—in each 2 kb window. Repeat that selection inside exons, genes, and
CDS so genic regions are intentionally covered, merge those lists, and add
planned special classes (breeding sites, population-private sites). The union
forms the capture list. Once a chip is made, compare its genotypes
against whole-genome calls on the same samples.

## Step by step

### 1. Start set: whole-genome SNPs on VS1

- Input: per-chromosome `Grape.${i}.pass_snp.vcf.gz` ([step 3](steps/03-maf-missingness.md)).
- Annotation: `VS1.final.gff3`, used for overlap counts and later for the genic selections ([step 1](steps/01-annotation-overlap.md), [step 2](steps/02-snp-function.md)).

### 2. Biallelic, MAF, and missingness filters

- First pass: `--max-missing 0.5 --maf 0.01 --min-alleles 2 --max-alleles 2` per chromosome, then merged ([step 3](steps/03-maf-missingness.md)).
- Later file names indicate a stricter set with MAF 0.05 and missingness 0.4 (`Grape.0_05maf_0_4mis_pass_snps_filtered.vcf.gz`). The notes say that filter "was already done"; its command was not pasted.
- Reading of the commands: biallelic sites match what a two-allele assay can score, and a minimum MAF removes sites that would be monomorphic in most samples. The notes do not state these reasons explicitly.

### 3. LD pruning: the knob for panel size

- `plink --indep-pairwise 50 5 <r2>` with r² 0.1, 0.3, and 0.5 on the loose set, and 0.1 on the strict set; file names also show 0.4 and 0.7 sets ([step 4](steps/04-ld-prune.md), [step 6](steps/06-maf-bed.md)).
- Reading of the commands: each r² cutoff yields a different site count, and subsequent steps were run across several cutoffs in parallel (ld01, ld03, ld04, ld05). Adjusting this cutoff controls the final site count. The notes do not record a specific target count.

### 4. Mean depth at least 10

- `vcftools --min-meanDP 10` on the pruned sets ([step 5](steps/05-mean-depth.md)). The notes say 10 reads.
- Reading of the commands: sites with low resequencing depth produce less reliable genotype calls and are poor panel candidates.

### 5. Score each site by minor allele frequency

- `vcftools --freq2`, after which the smaller of the two allele frequencies is written as the BED score on a 1 bp interval (`ld03_maf2bed.bed`) ([step 6](steps/06-maf-bed.md)).
- The notes say plink `--freq` was not usable for this.

### 6. One site per 2 kb window, highest MAF wins

- `bedtools makewindows -w 2000`, intersect with the MAF BED, `groupby ... -o max`, and keep the site whose score matches the window maximum ([step 8](steps/08-window-2kb.md)).
- This is the spacing rule of the panel. Reading of the commands: it distributes sites across every chromosome and keeps the most polymorphic site within each window.
- The notes record two failed attempts before this worked: sorting by score did not yield one site per window, and `groupby -full` retained the wrong row.
- An earlier idea using 25/24 bp windows around each site was abandoned. The notes say the blocks overlapped and that a 25 bp window means nothing when windows touch; the 2 kb window replaced it ([step 12](steps/12-flank.md)).

### 7. The same pick inside exons, genes, and CDS

- The window selection is repeated on features extracted from `VS1.final.gff3`—exon, gene, and CDS ([step 9](steps/09-exon-gene-cds.md))—and merged with `sort | uniq` ([step 10](steps/10-merge-functional.md)).
- Reading of the commands: this ensures genic sequence is deliberately covered rather than relying solely on genome-wide windows.
- The notes caution that a single site can overlap multiple features due to alternative splicing, requiring deduplication starting from the first intersect.
- SNP effects were also annotated with ANNOVAR (`--buildver VS1`), and PROVEAN was noted for missense sites, labeling scores below -2.5 as deleterious ([step 2](steps/02-snp-function.md)). The notes do not indicate that these labels were used to select sites.

### 8. Special site classes (planned, not scripted)

From [step 11](steps/11-extra-site-classes.md):

- Sites carried over from an earlier 10k set.
- Breeding sites: per-population MAF above 0.2 in at least half of the groups, plus GWAS hits.
- Private sites: MAF 0 within one population and very low across the others.

No command or output file was recorded for any of these; they represent design intentions only.

### 9. Probe flanks and coordinate checks

- A 50 bp flank extraction appears only as a heading. One site was checked using `blastn -task megablast` against `v4_genome_ref.fasta` ([step 12](steps/12-flank.md)).
- This is a single-site coordinate check; a full flank and probe-design step is absent from the notes.

### 10. Freeze

- The capture list is the union of the merged genic list, the 2 kb list, and `panel_raw.vcf.gz` ([step 13](steps/13-freeze.md)).
- The notes list vendor (Illumina) scoring as the final step and state that three file formats are required. Neither the formats nor a command was recorded, and the final site count was not noted.

## Checking a panel after it is made

[../notes/stat_array.md](../notes/stat_array.md) and `scripts/stat_italy/` contain the checks run on capture data:

- Genotype agreement between capture and whole-genome calls on the same samples, split into change types such as 0/1 to 0/0 (`scripts/stat_italy/hete2homo.py`; synthetic example in `scripts/stat_italy/example_synthetic/`). The script compares the two files row by row, requiring identical sites in the same order and identical samples in the same columns; it now halts if they diverge (checking CHROM, POS, REF, and ALT).
- Per-sample missing rate with `bcftools`, and library complexity with `preseq c_curve`.
- Mapped-rate change before and after capture, and before and after PCR (`group4_capeff.py`, `pcr_bias/mappedrate_fold.py`, `dna_probe/group2_map.py`).
- Site-level summaries: MAF distribution, spacing between adjacent sites, heterozygosity, and missing rate (`scripts/stat_vcf/`, `scripts/stat_array/`).

## What is missing

- The command for the MAF 0.05 / missingness 0.4 filter, the r² 0.4 and 0.7 prunes, and `get_keep.pl`.
- Population definitions for the per-group split ([step 7](steps/07-population-split.md)).
- Any script for breeding, private, or GWAS sites.
- Probe design, vendor scoring, and the final site count.
- A separate SR4R-style branch (minimal markers, Beagle, indels) was started and left unfinished ([step 14](steps/14-sr4r-branch.md)).
