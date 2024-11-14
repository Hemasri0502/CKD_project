import pandas as pd

# Load the XPT file
xpt_file = 'DR1TOT_I.XPT'  # Replace with the path to your XPT file
df = pd.read_sas(xpt_file, format='xport')

# Save as CSV
csv_file = 'DR1TOT_I.csv'  # Replace with your desired output CSV file path
df.to_csv(csv_file, index=False)

print(f"File has been successfully converted to {csv_file}")
