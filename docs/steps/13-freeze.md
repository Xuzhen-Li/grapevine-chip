# 13. What the notes call the capture freeze

## Input

- Lines 552–554: Illumina scoring is placed as the last step. The notes say to prepare three file formats.
- Lines 907–909, `##final` and `#1 capture`.
- Inputs named on the pasted line: `ld05_maf05mis04dp10_gff3_final_uniq.txt`, `ld05maf05mis04dp10_2kb.maf_array_pos.txt`, and `panel_raw.vcf.gz`.

## Do

```bash
cat ld05_maf05mis04dp10_gff3_final_uniq.txt ld05maf05mis04dp10_2kb.maf_array_pos.txt panel_raw.vcf.gz | sort | uniq | wc -l
```

## Get

- No formats and no command were written for the Illumina scoring step.
- The third input is a VCF filename. The notes do not record the `wc -l` result.
- Do not treat this line as a cleaned site list.
