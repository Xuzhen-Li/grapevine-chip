# 12. Flank sequence

## Input

- Line 41 is a heading only: extract flank 50 with prel. No command under that heading.
- Lines 521–542: `vcftools --freq2` again, a site BED, then the awk below, and a commented `bedtools flank`.
- Local `00_array/lifeover/megablast.sh` (25 lines, itself wrapped in a markdown fence) sets `FLANK=100` for chromosome 1 position 3055017.
- `lifeover/make_chain_file.sh` is a UCSC same-species liftover setup. Its download example is *Glycine max*, not the grapevine panel.

## Do

```bash
vcftools --freq2
awk 'NR==1 {next}{print $1"\t"$2-25"\t"$2+24}'
bedtools flank -i ld03_maf2sites.bed -g VS1.final.fa.2col.bed -l 25 -r 24
00_array/lifeover/megablast.sh
samtools faidx
blastn -task megablast
lifeover/make_chain_file.sh
```

## Get

- Groupby on the 25/24 windows is then rejected in the notes: overlapping blocks, and a 25 bp window has no meaning if adjacent windows touch. The 2 kb window (step 8) is what the notes say replaced this.
- `megablast.sh` runs `samtools faidx` on `VS1.final.fa` and `blastn -task megablast` against `v4_genome_ref.fasta`. One alignment row is pasted under the command. This is a single-site coordinate check, not the panel flank step.
