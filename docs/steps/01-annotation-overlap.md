# 1. Look at where reads and sites fall on the annotation

## Input

- Recorded in the local notebook at lines 3–36, under this step.
- `VS1.final.gff3` for where captured sites fall on features.
- `final_capture_ld05maf05mis04dp10_2kb_gff3_10kpanel_maf.bed` against `annotation.gff3` for one pasted count.
- Lines 44–164 are pasted cluster jobs that turn BAM depth or panel positions into CMplot density CSVs.

## Do

```bash
samtools depth
sambamba depth -t 10 -w 500
bedtools intersect
qualimap bamqc
```

## Get

- `samtools depth` and `sambamba depth -t 10 -w 500` are written as ways to see base or window depth.
- `bedtools intersect` against `VS1.final.gff3` is written to count how captured sites fall on features.
- Overlap counts pasted from `final_capture_ld05maf05mis04dp10_2kb_gff3_10kpanel_maf.bed` against `annotation.gff3`: `.` 45212, CDS 50292, exon 60112, five_prime_UTR 4100, gene 116589, mRNA 125290, TandemRepeat 9773, TEprotein 1113, three_prime_UTR 5720, Transposon 112874.
- The next line says this still drops some regions. These are overlap counts in the notes, not a frozen panel size.
- The later cluster jobs use `samtools depth`, drop `HiC_scaffold`, and `qualimap bamqc`. They are sample-coverage pictures, not site selection.
