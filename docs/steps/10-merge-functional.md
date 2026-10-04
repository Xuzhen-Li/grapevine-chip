# 10. Merge functional positions

## Input

- Recorded in the local notebook at lines 493–494 and 898–905.
- CDS, exon, and gene `*.maf_array_pos.txt`, for the unpruned set and for r² 0.5, 0.3, 0.1, and 0.4.

## Do

```bash
cat *.maf_array_pos.txt | sort|uniq
```

## Get

- `ld05_maf05mis04dp10_gff3_final_uniq.txt` and the ld03, ld01, and ld04 twins.
