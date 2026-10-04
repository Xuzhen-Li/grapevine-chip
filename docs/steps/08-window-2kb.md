## 8. One highest-MAF site per 2 kb window

Lines 411–440 (a fenced bash block the notes mark `###final` for the window pick) and lines 595–627 (`##method 2`, a pasted SLURM script).

Window file:

`bedtools makewindows -g VS1.final.fa.2col.bed -w 2000 > VS1.window.bed`

Then, for each LD set: intersect window BED with the MAF BED, `bedtools groupby -g 1,2,3 -c 5 -o max`, intersect back, and keep rows where the site score equals the window max (`awk '{if($5==$9) ...}'`). Positions go to `ld{01,03,04,05}maf05mis04dp10_2kb.maf_array_pos.txt`. `vcftools --positions` extracts a VCF from the matching `core.0.4mis0.05maf.ld0.*.snp_dp10.vcf.gz`.

The notes before the working version say a `sort` by score did not pick one site per window (row counts jumped between about 18万 and 140万 in the note text) and that `groupby -full` kept the wrong row. Those attempts are failed drafts in the same section, not a second method.

Lines 814–830 (`##method 7`, pasted SLURM, `#2kb`) repeat the 2 kb max pick on `core.0.4mis0.05maf.snp_dp10.vcf.gz` (no LD in the filename). The freq2 awk in that script reads `total_ld_freq2`, not `total_ld_freq2.frq`.

Back to [the step list](../steps.md).
