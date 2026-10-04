# 8. One highest-MAF site per 2 kb window

## Input

- Recorded in the local notebook at lines 411–440 (a fenced bash block the notes mark `###final` for the window pick) and lines 595–627 (`##method 2`, a pasted cluster script).
- Window genome file: `VS1.final.fa.2col.bed`.
- For each LD set, the MAF BED from step 6, and the matching `core.0.4mis0.05maf.ld0.*.snp_dp10.vcf.gz`.
- Lines 814–830 (`##method 7`, pasted cluster script, `#2kb`) repeat the 2 kb max pick on `core.0.4mis0.05maf.snp_dp10.vcf.gz` (no LD in the filename).

## Do

```bash
bedtools makewindows -g VS1.final.fa.2col.bed -w 2000 > VS1.window.bed
bedtools intersect
bedtools groupby -g 1,2,3 -c 5 -o max
awk '{if($5==$9) ...}'
vcftools --positions
```

## Get

- Positions go to `ld{01,03,04,05}maf05mis04dp10_2kb.maf_array_pos.txt`.
- `vcftools --positions` extracts a VCF from the matching `core.0.4mis0.05maf.ld0.*.snp_dp10.vcf.gz`.
- For each LD set the notes intersect the window BED with the MAF BED, run `bedtools groupby -g 1,2,3 -c 5 -o max`, intersect back, and keep rows where the site score equals the window max.
- The notes before the working version say a `sort` by score did not pick one site per window (row counts jumped between about 18 and 140 times ten thousand in the note text) and that `groupby -full` kept the wrong row. Those attempts are failed drafts in the same section, not a second method.
- The freq2 awk in the method 7 script reads `total_ld_freq2`, not `total_ld_freq2.frq`.
