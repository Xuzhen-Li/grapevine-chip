## Local files checked and not used as steps

| path under `00_array` | what it is |
| --- | --- |
| `intervalpos&region.py` | Interval tree of `wgs.pos` against `fianl_pos.txt`. One-off overlap of local position files. |
| `matched_intervals.py` | Matches `dedup_overlaps_region.txt` to probe-cover rows in `WGStest.csv`. One-off. |
| `stat_vcf_from_3527/maf_distribution.py` | Histogram of a chip MAF BED. |
| `stat_vcf_from_3527/pos_interval_stat.py` | Distance between adjacent sites, plotted. |
| `stat_vcf_from_3527/stat_rate.py` | Boxplot of het and missing rates. |

Those are checks or plots on data already in hand. They are not steps of the design path above.

Back to [the step list](../steps.md).
