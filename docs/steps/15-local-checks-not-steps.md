# 15. Local files checked and not used as steps

## Input

- Paths under `00_array`.
- `wgs.pos` against `fianl_pos.txt` in `intervalpos&region.py`.
- `dedup_overlaps_region.txt` and probe-cover rows in `WGStest.csv` for `matched_intervals.py`.
- A chip MAF BED for `stat_vcf_from_3527/maf_distribution.py`.
- Adjacent sites for `stat_vcf_from_3527/pos_interval_stat.py`.
- Het and missing rates for `stat_vcf_from_3527/stat_rate.py`.

## Do

```bash
intervalpos&region.py
matched_intervals.py
stat_vcf_from_3527/maf_distribution.py
stat_vcf_from_3527/pos_interval_stat.py
stat_vcf_from_3527/stat_rate.py
```

## Get

- `intervalpos&region.py`: an interval tree. One-off overlap of local position files.
- `matched_intervals.py`: matches `dedup_overlaps_region.txt` to probe-cover rows in `WGStest.csv`. One-off.
- `maf_distribution.py`: a histogram of a chip MAF BED.
- `pos_interval_stat.py`: distance between adjacent sites, plotted.
- `stat_rate.py`: a boxplot of het and missing rates.
- Those are checks or plots on data already in hand. They are not steps of the design path above.
