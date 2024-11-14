import pandas as pd

# List of CSV files to merge
csv_files = [
    'Albumin_Creatine.csv',   # Albumin & Creatinine - Urine file
    'Standard_Biochemistry.csv',  # Bioprofile file
    'Blood_Pressure.csv',    # Blood Pressure
    'Demo_Samples.csv',   # Demographics file
    'Diabetics.csv',    # Diabetes file
    'MCQ.csv',    # Medical conditions file
    'Dietary_Intakes.csv'  # Dietary file
]

# Load the first file as the base dataframe
df_merged = pd.read_csv(csv_files[0])

# Merge subsequent files based on SEQN
for file in csv_files[1:]:
    df = pd.read_csv(file)
    
    # Remove unnamed columns from both dataframes before merging
    df_merged = df_merged.loc[:, ~df_merged.columns.str.contains('^Unnamed')]
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
    # Merge and handle duplicate columns by adding suffixes if necessary
    df_merged = pd.merge(df_merged, df, on='SEQN', how='inner', suffixes=('_x', '_y'))
    
    # Drop duplicate columns caused by the merge (optional: you can customize this)
    df_merged = df_merged.loc[:, ~df_merged.columns.duplicated()]

# Save the merged dataset to a new CSV file
merged_csv_file = 'Merged_data2.csv'
df_merged.to_csv(merged_csv_file, index=False)

print(f"Merged dataset saved as {merged_csv_file}")
