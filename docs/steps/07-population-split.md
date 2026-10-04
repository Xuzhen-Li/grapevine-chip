# 7. Split named populations

## Input

- Recorded in the local notebook at lines 390–406.
- Groups written in the notes: `CG1-6`, `WWE12`, `WEE12`.
- A loop over `*.info` files writes cluster scripts.
- The VCF those scripts keep is the MAF 0.05 and missingness 0.4 VCF.
- The notebook does not define the groups.

## Do

```bash
vcftools --keep
```

## Get

- One kept VCF per `*.info` group named above. No output filename is written in this step.
