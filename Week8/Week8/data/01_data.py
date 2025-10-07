import pandas as pd
import unicodedata
import re


def clean_text(text):
    if isinstance(text, str):
        # Normalize Unicode characters
        norm_text = unicodedata.normalize('NFKC', text)
        return re.sub(r'[\x00-\x1f\x7f-\x9f]', '', norm_text)
    return text

try:
    df = pd.read_csv(r'full_dataset.csv', encoding='utf-8')
except FileNotFoundError:
    print("Error: 'full_dataset.csv' not found.")
    exit(1)

print("Columns to clean:", df.select_dtypes(include='object').columns)
print("First row before cleaning:", df.iloc[0])

# Apply cleaning to all string columns
for col in df.select_dtypes(include='object').columns:
    df[col] = df[col].apply(clean_text)


print("First row after cleaning:", df.iloc[0])

# Save cleaned DataFrame
df.to_csv('full_dataset_cleaned.csv', index=False, encoding='utf-8')
print("Cleaned data saved to 'full_dataset_cleaned.csv'")


# Print header of the cleaned CSV
df_cleaned = pd.read_csv('full_dataset_cleaned.csv', encoding='utf-8', sep=',', quoting=0)
print("Header of 'full_dataset_cleaned.csv':")
print(df_cleaned.head())

## Note to self - need to check for tab characters in the dataset..

