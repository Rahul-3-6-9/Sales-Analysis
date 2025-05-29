import pandas as pd

# Creating DataFrame with the encoding
df = pd.read_csv("Sample - Superstore.csv", encoding='latin1')

print(df.info())
print(df.describe())
print(df.head())

# Converting the date columns
df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
df['Ship Date'] = pd.to_datetime(df['Ship Date'], errors='coerce')

# Looking for any null value - if present
print(df.isnull().sum())

# Save cleaned version
df.to_csv("cleaned_data_superstore.csv", index=False)

print("Data cleaned and saved successfully!")
