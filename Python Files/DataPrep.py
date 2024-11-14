import pandas as pd
from sklearn.preprocessing import StandardScaler

# Load the csv file
df=pd.read_csv('Filtered_imp.csv')
print(df.head())

# Fill missing values with column mean (or you can use median)
df.fillna(df.mean(), inplace=True)

# Check for any remaining missing values
print(df.isnull().sum())

columns_to_exclude = ['SEQN', 'DIQ010', 'DID040', 'DIQ160', 'DIQ175H', 'DIQ175I', 'DIQ175T']

# Get the list of numeric columns that can be scaled
numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

# Exclude the columns that should not be scaled
columns_to_scale = [col for col in numeric_columns if col not in columns_to_exclude]

# Apply scaling only to continuous numeric columns
scaler = StandardScaler()  # or MinMaxScaler()
df[columns_to_scale] = scaler.fit_transform(df[columns_to_scale])

df = pd.get_dummies(df, columns=['DIQ010', 'DIQ175H', 'DIQ175I', 'DIQ175T'], drop_first=True)

# View the scaled dataset
print(df.head())

