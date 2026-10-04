# Design steps

Source: local notebook `00_array/##芯片位点处理全流程.md` (1836 lines). Line numbers below are that file. Commands were copied out of a working notebook. A block that starts with `#!/bin/bash` and `#SBATCH` is a pasted cluster job, not a command this repository runs or supports. Cluster paths under `/public/gxyy/...` are left as names of what the notes point at; they are not reproduced here as a recipe.

Sequencing results stay off GitHub. This file does not include VCFs, BAMs, or probe tables.

Each step is its own file.


- [1. Look at where reads and sites fall on the annotation](steps/01-annotation-overlap.md)
- [2. Annotate SNP function](steps/02-snp-function.md)
- [3. Filter MAF and missingness](steps/03-maf-missingness.md)
- [4. LD prune](steps/04-ld-prune.md)
- [5. Mean depth](steps/05-mean-depth.md)
- [6. Recompute MAF and make a BED](steps/06-maf-bed.md)
- [7. Split named populations](steps/07-population-split.md)
- [8. One highest-MAF site per 2 kb window](steps/08-window-2kb.md)
- [9. Same pick on exon, gene, and CDS](steps/09-exon-gene-cds.md)
- [10. Merge functional positions](steps/10-merge-functional.md)
- [11. Sites the notes add but do not script](steps/11-extra-site-classes.md)
- [12. Flank sequence](steps/12-flank.md)
- [13. What the notes call the capture freeze](steps/13-freeze.md)
- [14. SR4R-style branch (separate, unfinished)](steps/14-sr4r-branch.md)
- [Local files checked and not used as steps](steps/15-local-checks-not-steps.md)
