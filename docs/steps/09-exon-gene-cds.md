# 9. Same pick on exon, gene, and CDS

## Input

- Recorded in the local notebook at lines 445–491 and 631–659 (exon, `##method 4`, pasted cluster script).
- Lines 689–693 build the BEDs.
- Lines 697–718 (gene, `##method 5`, pasted cluster script). The rest of that script matches the exon pattern through `vcftools --positions`.
- CDS is `##method 6` (heading at line 756) and the same intersect, groupby, and max pattern.
- Method 7 lines 831–839 paste the CDS and exon half of that pattern on the unpruned set.
- `VS1.final.gff3`.

## Do

```bash
awk -v OFS="\t" '{if($3=="exon") print $0}' VS1.final.gff3
bedtools intersect
bedtools groupby
vcftools --positions
sort|uniq
wc -l
```

## Get

- Gene and CDS use the same awk with `$3=="gene"` and `$3=="CDS"`, then chromosome, start, and end, then `sort|uniq`.
- The notes (lines 454–491) say exon counts did not match expectations because of alternative splicing: one site falls in more than one feature, so dedup has to start from the first intersect.
- They also say the assembly is Hi-C named, the GFF is numeric, and the freq file may be chromosomes only.
- A pasted `wc -l` (lines 662–685) records intermediate file lengths, including `VS1.final.exon.bed` 171237 lines and `ld05maf05mis04dp10_exon.maf_array_pos.txt` 51217 lines.
- Those are file lengths in the notes, not a released panel size.
