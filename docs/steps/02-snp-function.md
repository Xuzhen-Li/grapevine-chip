# 2. Annotate SNP function

## Input

- Recorded in the local notebook at lines 167–222, under this step.
- `VS1.final.gff3` and `VS1.final.fa`.
- A later pasted cluster job (lines 198–209) subsets `Grape.pass_biallel.vcf.gz` with `--positions` on `final_capture_ld05maf05mis04dp10_2kb_gff3_10kpanel_maf.txt` before the same annotation.
- `Grape.pass.variant_function` for the pasted `uniq -c` counts.
- PROVEAN is described for missense sites. No local PROVEAN script is in `00_array`.
- `vcf2annovar.py` is not in the local `00_array` folder.

## Do

```bash
gff3ToGenePred
retrieve_seq_from_fasta.pl
python vcf2annovar.py
annotate_variation.pl --buildver VS1 --geneanno
uniq -c
```

## Get

- `gff3ToGenePred` on `VS1.final.gff3`, then `retrieve_seq_from_fasta.pl` on `VS1.final.fa`.
- `python vcf2annovar.py` writes a five-column ANNOVAR file: chromosome, start, end, ref, alt.
- `annotate_variation.pl --buildver VS1 --geneanno`.
- `uniq -c` on `Grape.pass.variant_function` is pasted as: downstream 11664, exonic 47999, exonic;splicing 1, intergenic 95593, intronic 58886, splicing 85, upstream 12335, upstream;downstream 1305, UTR3 4891, UTR5 3501.
- The notes say a PROVEAN score less than -2.5 is deleterious and other scores are neutral.
- The old NR, PSI-BLAST, CD-HIT, and blastdbcmd versions have to match PROVEAN. CD-HIT v4.0 is the version named.
