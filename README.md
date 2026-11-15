# grapevine-chip

Notes on how a grapevine SNP capture panel was designed: which sites were
kept, how they were spaced, and why. Start with
[docs/DESIGN_RATIONALE.md](docs/DESIGN_RATIONALE.md).

This is a record of one design, written from a working notebook. It is not
a pipeline you can run end to end. Many commands are pasted cluster (SLURM)
jobs with paths that only existed on that cluster. VCFs, BAMs, and probe
tables are not in the repository.

To analyze data from a chip you already have, use
[gtbs-chip-service-kit](https://github.com/Xuzhen-Li/gtbs-chip-service-kit).
The grapevine 167K walkthrough is in
[grapeancestry](https://github.com/Xuzhen-Li/grapeancestry) (demo report:
[ramos2019_np.batch.report.html](https://xuzhen-li.github.io/grapeancestry/demo/results/ramos2019_np.batch.report.html)).

## Design in short

1. Start from whole-genome SNP calls on the VS1 reference (19 chromosomes).
2. Keep biallelic SNPs; filter by MAF and missingness (0.01/0.5 loose, 0.05/0.4 strict).
3. LD-prune with `plink --indep-pairwise 50 5 r²` at several r² cutoffs. The cutoff sets the panel size.
4. Keep sites with mean depth of at least 10.
5. Score each site by minor allele frequency.
6. Keep one site per 2 kb window, the one with the highest MAF.
7. Repeat that pick inside exons, genes, and CDS, and merge.
8. Add planned classes (breeding sites, population-private sites). These were never scripted.
9. Freeze the union. Vendor scoring was planned as the last step and not recorded.

After the chip is made, compare its genotypes with the whole-genome calls on
the same samples (`scripts/stat_italy/hete2homo.py`; a synthetic example is in
`scripts/stat_italy/example_synthetic/`).

## Source

The steps follow a local notebook in a folder named `00_array`. Reference names in that notebook are `VS1.final.fa` and `VS1.final.gff3`. Chromosome count used with plink is `--chr-set 19`.

## Step files

One file per step, each split into Input, Do, and Get. Index: [docs/steps.md](docs/steps.md).

1. [Where reads and sites fall](docs/steps/01-annotation-overlap.md)
2. [SNP function](docs/steps/02-snp-function.md)
3. [MAF and missingness](docs/steps/03-maf-missingness.md)
4. [LD prune](docs/steps/04-ld-prune.md)
5. [Mean depth](docs/steps/05-mean-depth.md)
6. [MAF bed](docs/steps/06-maf-bed.md)
7. [Named populations](docs/steps/07-population-split.md)
8. [One site per 2 kb](docs/steps/08-window-2kb.md)
9. [Exon, gene, and CDS](docs/steps/09-exon-gene-cds.md)
10. [Merge functional positions](docs/steps/10-merge-functional.md)
11. [Site classes with no script](docs/steps/11-extra-site-classes.md)
12. [Flank](docs/steps/12-flank.md)
13. [Capture freeze](docs/steps/13-freeze.md)
14. [Unfinished SR4R branch](docs/steps/14-sr4r-branch.md)

Author: Xuzhen Li ([ORCID](https://orcid.org/0000-0003-3670-6657))
