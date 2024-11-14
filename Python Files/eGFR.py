import pandas as pd
df = pd.read_csv('Filtered_imp.csv')
# Mapping for sex column
def map_sex(val):
    if val == 1:  # 1 corresponds to Male
        return 'male'
    elif val == 2:  # 2 corresponds to Female
        return 'female'
    else:
        return 'unknown'

# Mapping for race based on RIDRETH1 (simplified for eGFR calculation)
def map_race(val):
    if val == 4:  # Non-Hispanic Black
        return 'african_american'
    else:
        return 'non_african_american'

# CKD-EPI eGFR calculation function
def calculate_egfr(scr, age, sex, race):
    if sex == 'female':
        k = 0.7
        alpha = -0.329
        gender_factor = 1.018
    else:
        k = 0.9
        alpha = -0.411
        gender_factor = 1
    
    # Race factor adjustment (1.159 for African Americans)
    race_factor = 1.159 if race == 'african_american' else 1
    
    # CKD-EPI formula for eGFR
    egfr = 141 * min(scr / k, 1) ** alpha * max(scr / k, 1) ** -1.209 * 0.993 ** age * gender_factor * race_factor
    return egfr

# Assuming df is your dataset DataFrame
# Map gender and race for the eGFR calculation
df['sex_mapped'] = df['RIAGENDR'].apply(map_sex)
df['race_mapped'] = df['RIDRETH1'].apply(map_race)

# Apply the eGFR calculation
df['eGFR'] = df.apply(lambda row: calculate_egfr(row['LBXSCR'], row['RIDAGEYR'], row['sex_mapped'], row['race_mapped']), axis=1)

# Print or inspect the results
# print(df[['SEQN', 'LBXSCR', 'eGFR']])
def assign_ckd_stage(egfr):
    if egfr >= 90:
        return 1  # Stage 1
    elif 60 <= egfr < 90:
        return 2  # Stage 2
    elif 45 <= egfr < 60:
        return 3.1  # Stage 3a
    elif 30 <= egfr < 45:
        return 3.2  # Stage 3b
    elif 15 <= egfr < 30:
        return 4  # Stage 4
    else:
        return 5  # Stage 5

# Apply the function to your dataset
df['CKD_stage'] = df['eGFR'].apply(assign_ckd_stage)

# Inspect the newly created column
print(df[['eGFR', 'CKD_stage']])
