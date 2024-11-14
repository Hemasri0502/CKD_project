import pandas as pd

# Read the CSV file
input_file = 'Merged_data2.csv'  # Update this with your actual file name
output_file = 'Filtered_imp_with_eGFR_CKD.csv'

# List of important columns you want to retain
important_columns = ['SEQN','URXUMA','URXUMS','URXUCR','URXCRS','URDACT', 
                     'LBXSAL','LBXSBU','LBXSCR','LBXSUA','LBXSPH',
                     'BPXSY1','BPXDI1','BPXSY2','BPXDI2','BPXSY3','BPXDI3',
                     'RIDSTATR','RIAGENDR','RIDAGEYR','RIDRETH1','DMDBORN4','DMDYRSUS','DMDHHSIZ','INDHHIN2','INDFMIN2','INDFMPIR',
                     'DIQ010','DID040','DIQ160','DIQ175H','DIQ175I','DIQ175T']

# Load the data into a DataFrame
df = pd.read_csv(input_file)

# Filter the DataFrame to retain only the important columns
filtered_df = df[important_columns]

# CKD-EPI eGFR calculation function
def calculate_egfr(scr, age, sex, race):
    if sex == 2:  # Female
        k = 0.7
        alpha = -0.329
        gender_factor = 1.018
    else:  # Male (1 corresponds to Male)
        k = 0.9
        alpha = -0.411
        gender_factor = 1
    
    # Race factor adjustment (1.159 for African Americans)
    race_factor = 1.159 if race == 4 else 1  # Non-Hispanic Black (race 4 in RIDRETH1)
    
    # CKD-EPI formula for eGFR
    egfr = 141 * min(scr / k, 1) ** alpha * max(scr / k, 1) ** -1.209 * 0.993 ** age * gender_factor * race_factor
    return egfr

# CKD Stage classification based on eGFR values
def classify_ckd_stage(egfr):
    if egfr >= 90:
        return int(1)  # Stage 1
    elif 60 <= egfr < 90:
        return int(2)  # Stage 2
    elif 45 <= egfr < 60:
        return int(3)  # Stage 3 (Combine 3a and 3b as a single class)
    elif 30 <= egfr < 45:
        return int(4)  # Stage 4
    elif 15 <= egfr < 30:
        return int(5)  # Stage 5

# Apply the eGFR calculation using original numeric columns
filtered_df['eGFR'] = filtered_df.apply(lambda row: calculate_egfr(row['LBXSCR'], row['RIDAGEYR'], row['RIAGENDR'], row['RIDRETH1']), axis=1)

# Apply the CKD stage classification based on eGFR
filtered_df['CKD_stage'] = filtered_df['eGFR'].apply(classify_ckd_stage)

# Preprocessing Step: Remove rows where eGFR is NaN (i.e., missing values)
filtered_df = filtered_df.dropna(subset=['eGFR'])

# Drop any unnecessary columns, like the categorical mappings ('sex_mapped', 'race_mapped') if they exist
# Since we are using the numeric columns, there are no additional categorical columns to remove

# Save the filtered DataFrame with eGFR and CKD stages to a new CSV file
filtered_df.to_csv(output_file, index=False)

print(f"Filtered CSV with eGFR and CKD stages saved to {output_file} (after removing missing eGFR values and categorical columns)")
