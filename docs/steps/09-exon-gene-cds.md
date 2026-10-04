## 9. Same pick on exon, gene, and CDS

Lines 445–491 and 631–659 (exon, `##method 4`, pasted SLURM). Lines 689–693 build the BEDs. Lines 697–718 (gene, `##method 5`, pasted SLURM; the rest of the script matches the exon pattern through `vcftools --positions`). CDS is `##method 6` (heading at line 756) and the same intersect / groupby / max pattern; method 7 lines 831–839 paste the CDS and exon half of that pattern on the unpruned set.

Exon BED:

`awk -v OFS="\t" '{if($3=="exon") print $0}' VS1.final.gff3`

then chromosome, start, end, `sort|uniq`. Gene and CDS use `$3=="gene"` and `$3=="CDS"`.

The notes (lines 454–491) say exon counts did not match expectations because of alternative splicing: one site falls in more than one feature, so dedup has to start from the first intersect. They also say the assembly is Hi-C named, the GFF is numeric, and the freq file may be chromosomes only. A pasted `wc -l` (lines 662–685) records intermediate file lengths, including `VS1.final.exon.bed` 171237 lines and `ld05maf05mis04dp10_exon.maf_array_pos.txt` 51217 lines. Those are file lengths in the notes, not a released panel size.

Back to [the step list](../steps.md).
