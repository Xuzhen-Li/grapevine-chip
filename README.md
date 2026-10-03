# grapevine-chip

How to design your own chip. This repo is the design path: choose sites, check them against the annotation, and freeze a panel. It is not a place to analyze data from a chip you already hold.

The notes below are the grapevine capture-panel path as written in a local working notebook. They are not a portable pipeline. Many blocks are pasted SLURM job scripts from one cluster, with absolute paths and a private partition. Sequencing results, VCFs, BAMs, and probe tables stay off GitHub.

The analysis suite for data you already have is [gtbs-chip-service-kit](https://github.com/Xuzhen-Li/gtbs-chip-service-kit) (genotyping by target sequencing). The grapevine 167K walkthrough stays in [grapeancestry](https://github.com/Xuzhen-Li/grapeancestry). Demo report: [ramos2019_np.batch.report.html](https://xuzhen-li.github.io/grapeancestry/demo/results/ramos2019_np.batch.report.html).

Step detail: [docs/steps.md](docs/steps.md).

## Where the steps came from

The ordered path is the notebook `##芯片位点处理全流程.md` in the local folder `00_array` (1836 lines). Reference names in that notebook are `VS1.final.fa` and `VS1.final.gff3`. Chromosome count used with plink is `--chr-set 19`.

## Design path

1. **Biallelic sites, then missingness and MAF.** Per chromosome, keep two alleles. Two filter sets are named. One is pasted as `vcftools --max-missing 0.5 --maf 0.01 --min-alleles 2 --max-alleles 2`, then `MergeVcfs` across chromosomes 1–19. The other is named MAF 0.05 and missingness 0.4 (`Grape.0_05maf_0_4mis_pass_snps_filtered.vcf.gz`); the notebook says that set already existed and does not paste its filter command.
2. **LD prune.** On the MAF 0.01 / missingness 0.5 set, plink `--indep-pairwise 50 5` at r² 0.5, 0.3, and 0.1, then a perl `get_keep.pl` (not in the local folder) to subset the VCF. On the MAF 0.05 / missingness 0.4 set, the only pasted prune is `--indep-pairwise 50 5 0.1`. Later filenames also use r² 0.4, 0.5, 0.7, and an unpruned `ldtotal`, without a pasted command for each.
3. **Depth.** Note text: limit reads per SNP to 10, implemented as `vcftools --min-meanDP 10` on the MAF 0.05 / missingness 0.4 LD VCFs (r² 0.3, 0.1, and 0.4 are the three commands pasted).
4. **MAF bed for ranking.** `vcftools --freq2`, then keep the smaller of the two allele-count columns as the rank score and write a 1 bp BED.
5. **Optional population split.** Groups named `CG1-6`, `WWE12`, and `WEE12` are pulled with `vcftools --keep` from the MAF 0.05 / missingness 0.4 VCF. The notebook does not define those labels.
6. **One site per 2 kb window.** `bedtools makewindows -w 2000` on a two-column genome file, intersect the MAF BED, `bedtools groupby` with `-o max`, keep the site whose score equals that max, write positions, `vcftools --positions`. This is "method 2" and is a pasted SLURM script. The same pattern is repeated on an unpruned depth-filtered VCF ("method 7", also a pasted SLURM script).
7. **Annotation overlap.** Exon, gene, and CDS intervals are cut from `VS1.final.gff3` and run through the same max-score pick (methods 4, 5, and 6; pasted SLURM). The notes say alternative splicing makes one site hit several features, and that the Hi-C assembly names and the numeric GFF names have to be checked before the overlap means anything. A separate ANNOVAR gene annotation and a PROVEAN missense check (score &lt; -2.5 called deleterious) are written earlier in the notebook; they are not the window pick.
8. **Unique functional positions.** `cat` of the CDS, exon, and gene position lists, then `sort | uniq`, done per LD cutoff including r² 0.5, 0.3, 0.1, and 0.4.
9. **Flank.** A heading says to extract flank 50 with perl and has no command. A later block builds 25 bp upstream and 24 bp downstream (`$2-25` to `$2+24`, and a commented `bedtools flank -l 25 -r 24`). The same notes say that overlapping windows make this pick wrong. A local `lifeover/megablast.sh` uses `FLANK=100` for one example site against another assembly; that is a coordinate check, not the panel freeze.
10. **Extra site classes, only as notes.** A "10k" block says the back-fill result already exists. Breeding sites: a note that at least half the populations should have MAF &gt; 0.2 (written with a question mark) and that typed sites come from GWAS. Population-private sites: MAF = 0 in one population and very small in the others. No command is pasted for these three.
11. **Freeze.** The notebook's `##final` / `#1 capture` block concatenates the r² 0.5 functional unique list, the r² 0.5 2 kb position list, and the filename `panel_raw.vcf.gz`, then `sort | uniq | wc -l`. No count is written after that command. Illumina scoring is marked as the last step ("prepare three file formats") with no formats and no command.

A second notebook stretch follows the rice SR4R tag / GWAS / minimal-marker layout (Beagle phasing, then minimal markers, plus an indel side branch). It is mostly pasted SLURM, records out-of-memory and temp-file failures, and is not a finished command set. See [docs/steps.md](docs/steps.md).

**Author:** Xuzhen Li · [ORCID](https://orcid.org/0000-0003-3670-6657)
