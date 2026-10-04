# grapevine-chip

How to design your own chip. This repo is the design path: choose sites, check them against the annotation, and freeze a panel. It is not a place to analyze data from a chip you already hold.

The notes below are the grapevine capture-panel path as written in a local working notebook. They are not a portable pipeline. Many blocks are pasted SLURM job scripts from one cluster, with absolute paths and a private partition. Sequencing results, VCFs, BAMs, and probe tables stay off GitHub.

The analysis suite for data you already have is [gtbs-chip-service-kit](https://github.com/Xuzhen-Li/gtbs-chip-service-kit) (genotyping by target sequencing). The grapevine 167K walkthrough stays in [grapeancestry](https://github.com/Xuzhen-Li/grapeancestry). Demo report: [ramos2019_np.batch.report.html](https://xuzhen-li.github.io/grapeancestry/demo/results/ramos2019_np.batch.report.html).

Step detail: [docs/steps.md](docs/steps.md).

## Where the steps came from

The ordered path is the local notebook in the local folder `00_array`. Reference names in that notebook are `VS1.final.fa` and `VS1.final.gff3`. Chromosome count used with plink is `--chr-set 19`.

## Design path

One file per step. Each file is Input, Do, and Get. The list is [docs/steps.md](docs/steps.md).

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

**Author:** Xuzhen Li · [ORCID](https://orcid.org/0000-0003-3670-6657)
