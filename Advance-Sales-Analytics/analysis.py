import pandas as pd

#load csv file
df = pd.read_csv("Advance-Sales-Analytics\data\sales.csv")

#====================
#BASIC INFORMATION
#======================

#show first 5row
print("\nFIRST FIVE ROWS: ",df.head(5))

print("\nDATASET SHAPE: ",df.shape)

print("\nCOLUMN NAMES: ",df.columns)

print("\nDATA TYPES: ",df.dtypes)

print("\nMISSING VALUES: ",df.isnull().sum())

print("\nSTATISTICAL SUMMARY: ",df.describe())

#====================
#DATA CLEANING
#====================

#Remove Duplicate rows
df = df.drop_duplicates()

#Fill missing values with mean 
numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns

for col in numeric_columns:
    df[col]= df[col].fillna(df[col].mean())

#Fill missing text values
text_columns = df.select_dtypes(include=['object']).columns

for col in text_columns:
    df[col] = df[col].fillna("Unknown")

#=======================
# CHECK AFTER CLEANING
# ======================

print("\n MISSING VALUES AFTER CLEANING",df.isnull().sum())

print("\n FINAL DATASET SHAPE",df.shape)

#Save cleaned dataset
df.to_csv("cleaned_sales.csv", index=False)

print("\nCleaned dataset saved successfully")

