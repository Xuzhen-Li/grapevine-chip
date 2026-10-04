## 2. Annotate SNP function

Lines 167–222, `SNP信息注释`.

1. `gff3ToGenePred` on `VS1.final.gff3`, then `retrieve_seq_from_fasta.pl` on `VS1.final.fa`.
2. `python vcf2annovar.py` to a five-column ANNOVAR file (chromosome, start, end, ref, alt). The converter is not in the local `00_array` folder.
3. `annotate_variation.pl --buildver VS1 --geneanno`.

A later pasted SLURM job (lines 198–209) subsets `Grape.pass_biallel.vcf.gz` with `--positions` on `final_capture_ld05maf05mis04dp10_2kb_gff3_10kpanel_maf.txt` before the same annotation. `uniq -c` on `Grape.pass.variant_function` is pasted as: downstream 11664, exonic 47999, exonic;splicing 1, intergenic 95593, intronic 58886, splicing 85, upstream 12335, upstream;downstream 1305, UTR3 4891, UTR5 3501.

PROVEAN is described for missense sites. The notes say a score less than -2.5 is deleterious and other scores are neutral, and that the old NR, PSI-BLAST, CD-HIT, and blastdbcmd versions have to match PROVEAN (CD-HIT v4.0 is the version named). No local PROVEAN script is in `00_array`.

Back to [the step list](../steps.md).
