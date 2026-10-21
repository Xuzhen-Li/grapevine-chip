# 示例输入见 example_synthetic/：wgs_genotypes.txt、cap_genotypes.txt（合成数据，不是真实样本）

############Data preparation##########

# base on bash 
## bcftools query -f '%CHROM\t%POS\t%REF\t%ALT[\t%SAMPLE=%GT]\n' wgs.vcf.gz  > wgs_genotypes.txt
## bcftools query -f '%CHROM\t%POS\t%REF\t%ALT[\t%SAMPLE=%GT]\n' cap.vcf.gz  > cap_genotypes.txt

############ Step 1: Basic Analysis of Homozygous and Heterozygous Variation##########
import pandas as pd

# Update these paths to match your file locations
path_wgs = "wgs_genotypes.txt"
path_cap = "cap_genotypes.txt"

# Load data
df_wgs = pd.read_csv(path_wgs, sep="\t", header=None)
df_cap = pd.read_csv(path_cap, sep="\t", header=None)

# Assuming the first four columns are chromosome, position, reference allele, and variant allele, respectively
# Remaining columns are sample genotypes
# For simplicity, convert genotype columns to a long format
df_wgs_long = df_wgs.melt(id_vars=[0,1,2,3], var_name="Sample", value_name="Genotype_wgs")
df_cap_long = df_cap.melt(id_vars=[0,1,2,3], var_name="Sample", value_name="Genotype_cap")

# Merge datasets for comparison
df_merged = pd.merge(df_wgs_long, df_cap_long, on=[0,1,"Sample"])

# Calculate consistency
df_merged['Consistent'] = df_merged['Genotype_wgs'] == df_merged['Genotype_cap']
consistency_rate = df_merged['Consistent'].mean()
print(f"Overall consistency rate: {consistency_rate*100:.2f}%")

# Analyze types of discrepancies
df_merged['Discrepancy_Type'] = None
df_merged.loc[df_merged['Genotype_wgs'] != df_merged['Genotype_cap'], 'Discrepancy_Type'] = df_merged.apply(
    lambda x: 'Hetero_to_Homo' if '0/1' in x['Genotype_wgs'] or '1/0' in x['Genotype_wgs'] else (
        'Homo_to_Hetero' if '0/0' in x['Genotype_cap'] or '1/1' in x['Genotype_cap'] else 'Other'), axis=1
)

discrepancy_counts = df_merged['Discrepancy_Type'].value_counts(normalize=True) * 100
print(discrepancy_counts)


############## Step 2: Detail Analysis of Homozygous and Heterozygous Variation###############
import pandas as pd
import numpy as np

# Adjust the file paths according to your file locations
path_to_wgs_file = 'wgs_genotypes.txt'
path_to_cap_file = 'cap_genotypes.txt'

# Load the files, assuming there is no header present
df_wgs = pd.read_csv(path_to_wgs_file, sep='\t', header=None)
df_cap = pd.read_csv(path_to_cap_file, sep='\t', header=None)

# Print the first few lines of the data to check them
print(df_wgs.head())
print(df_cap.head())

# Select a sample column to inspect genotype formats, assuming it is the 5th column
sample_genotypes_wgs = df_wgs.iloc[:, 4]
sample_genotypes_cap = df_cap.iloc[:, 4]

# Print the unique genotype data to check the formats
print(sample_genotypes_wgs.unique())
print(sample_genotypes_cap.unique())

# Clean the genotype data by removing sample name prefixes
for col in df_wgs.columns[4:]:
    df_wgs[col] = df_wgs[col].str.split('=').str[1]
    df_cap[col] = df_cap[col].str.split('=').str[1]

# Check the unique values of genotype data again
print(df_wgs.iloc[:, 4].unique())
print(df_cap.iloc[:, 4].unique())

# Initialize a dictionary to keep track of discrepancy types
discrepancy_types = {
    '0/0→0/1': 0,
    '0/0→1/1': 0,
    '0/1→0/0': 0,
    '0/1→1/1': 0,
    '1/1→0/0': 0,
    '1/1→0/1': 0,
    'Consistent': 0
}

# Iterate over all loci for each sample to compare genotypes
for col in df_wgs.columns[4:]:
    for i in range(len(df_wgs)):
        genotype_wgs = df_wgs[col].iat[i]
        genotype_cap = df_cap[col].iat[i]
        # To simplify, we do not consider genotypes containing '2'
        if '2' in genotype_wgs or '2' in genotype_cap:
            continue
        # Construct the key for the discrepancy type
        key = f'{genotype_wgs}→{genotype_cap}'
        # Increase the count for the discrepancy type, or count it as consistent
        if genotype_wgs == genotype_cap:
            discrepancy_types['Consistent'] += 1
        elif key in discrepancy_types:
            discrepancy_types[key] += 1
        else:
            # If a new discrepancy type is encountered, it can be added to the dictionary
            discrepancy_types[key] = discrepancy_types.get(key, 0) + 1

# Output the discrepancy statistics
print(discrepancy_types)

# Calculate the percentage and standard error for each type of discrepancy
total_discrepancies = sum(discrepancy_types.values()) - discrepancy_types['Consistent']
discrepancy_proportions = {k: (v / total_discrepancies * 100) for k, v in discrepancy_types.items() if k != 'Consistent'}
discrepancy_se = {k: np.sqrt((prop / 100 * (1 - prop / 100)) / total_discrepancies) * 100 for k, prop in discrepancy_proportions.items()}

# Print results
for k, v in discrepancy_proportions.items():
    print(f"{k}: {v:.2f}% (SE: {discrepancy_se[k]:.2f}%)")


############## Step 3: Detail Analysis of Homozygous and Heterozygous Variation in Each sample###############
import pandas as pd
import numpy as np

# Update these file paths according to where your files are located
path_to_wgs_file = 'wgs_genotypes.txt'
path_to_cap_file = 'cap_genotypes.txt'

# Try to read the files assuming there is no header
df_wgs = pd.read_csv(path_to_wgs_file, sep='\t', header=None)
df_cap = pd.read_csv(path_to_cap_file, sep='\t', header=None)

# Print the first few rows of the data to inspect them
print(df_wgs.head())
print(df_cap.head())

# Choose a column to check the genotype format, assuming it is the 5th column
sample_genotypes_wgs = df_wgs.iloc[:, 4]
sample_genotypes_cap = df_cap.iloc[:, 4]

# Print the unique values of the genotype data to check the formats
print(sample_genotypes_wgs.unique())
print(sample_genotypes_cap.unique())

# Clean the genotype data by removing sample name prefixes
for col in df_wgs.columns[4:]:
    df_wgs[col] = df_wgs[col].str.split('=').str[1]
    df_cap[col] = df_cap[col].str.split('=').str[1]

# Check the unique values of genotype data again
print(df_wgs.iloc[:, 4].unique())
print(df_cap.iloc[:, 4].unique())

# Assume df_wgs and df_cap are the cleaned DataFrames and sample_columns are the list of sample column names
sample_columns = df_wgs.columns[4:]  # Assuming genotype information starts from the 5th column

# Iterate over each sample to calculate consistency, discrepancies, and variation types
for sample in sample_columns:
    consistent = 0
    discrepancies = 0
    discrepant_positions = []
    variation_stats = {'0/0→0/1': 0, '0/0→1/1': 0, '0/1→0/0': 0, '0/1→1/1': 0, '1/1→0/0': 0, '1/1→0/1': 0, 'Consistent': 0, 'Other': 0}
    
    for i in range(len(df_wgs)):
        genotype_wgs = df_wgs[sample].iat[i].split('=')[-1]
        genotype_cap = df_cap[sample].iat[i].split('=')[-1]
        
        # Check for consistency
        if genotype_wgs == genotype_cap:
            consistent += 1
            variation_stats['Consistent'] += 1
        else:
            discrepancies += 1
            discrepant_position = {'CHROM': df_wgs[0].iat[i], 'POS': df_wgs[1].iat[i], 'wgs': genotype_wgs, 'cap': genotype_cap}
            discrepant_positions.append(discrepant_position)
            change_key = f'{genotype_wgs}→{genotype_cap}'
            variation_stats[change_key] = variation_stats.get(change_key, 0) + 1
    
    # Calculate percentages
    total_positions = consistent + discrepancies
    consistent_pct = (consistent / total_positions * 100) if total_positions else 0
    discrepancies_pct = (discrepancies / total_positions * 100) if total_positions else 0
    
    # Print consistency and discrepancy statistics for each sample
    print(f"Sample: {sample}")
    print(f"Consistent: {consistent} ({consistent_pct:.2f}%)")
    print(f"Discrepancies: {discrepancies} ({discrepancies_pct:.2f}%)")
    print("Variation Stats:")
    for variation, count in variation_stats.items():
        print(f"  {variation}: {count}")
    print(f"Discrepant Positions (first 5): {discrepant_positions[:5]}")
    print('---')

