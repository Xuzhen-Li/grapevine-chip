## 12. Flank sequence

- Line 41, `利用prel提取flank50`: heading only.
- Lines 521–542: `vcftools --freq2` again, site BED, then `awk 'NR==1 {next}{print $1"\t"$2-25"\t"$2+24}'` and a commented `bedtools flank -i ld03_maf2sites.bed -g VS1.final.fa.2col.bed -l 25 -r 24`. Groupby on the 25/24 windows is then rejected in the notes: overlapping blocks, and a 25 bp window "必然没有意义" if adjacent windows touch. The 2 kb window (step 8) is what the notes say replaced this.
- Local `00_array/lifeover/megablast.sh` (25 lines, itself wrapped in a markdown fence) sets `FLANK=100` for chromosome 1 position 3055017, `samtools faidx` on `VS1.final.fa`, and `blastn -task megablast` against `v4_genome_ref.fasta`. One alignment row is pasted under the command. This is a single-site coordinate check, not the panel flank step. `lifeover/make_chain_file.sh` is a UCSC same-species liftover setup whose download example is *Glycine max*, not the grapevine panel.

Back to [the step list](../steps.md).
