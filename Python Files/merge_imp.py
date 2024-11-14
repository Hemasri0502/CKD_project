import pandas as pd

# Read the CSV file
input_file = 'Merged_data2.csv'  # Update this with your actual file name
output_file = 'Filtered_imp.csv'

# List of important columns you want to retain
important_columns = ['SEQN','URXUMA','URXUMS','URXUCR','URXCRS','URDACT', 
                     'LBXSAL','LBXSBU','LBXSCR','LBXSUA','LBXSPH',
                     'BPXSY1','BPXDI1','BPXSY2','BPXDI2','BPXSY3','BPXDI3',
                     'RIDSTATR','RIAGENDR','RIDAGEYR','RIDRETH1','DMDBORN4','DMDYRSUS','DMDHHSIZ','INDHHIN2','INDFMIN2','INDFMPIR',
                     'DIQ010','DID040','DIQ160','DIQ175H','DIQ175I','DIQ175T'
    
]

# Load the data into a DataFrame
df = pd.read_csv(input_file)
print(df.columns)

# Filter the DataFrame to retain only the important columns
filtered_df = df[important_columns]

# Save the filtered DataFrame to a new CSV file
filtered_df.to_csv(output_file, index=False)

print(f"Filtered CSV saved to {output_file}")
