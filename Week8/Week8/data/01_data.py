import pandas as pd
import unicodedata
import re


def clean_text(text):
    if isinstance(text, str):
        norm_text = unicodedata.normalize('NFKC', text)
        return re.sub(r'[\x00-\x1f\x7f-\x9f]', '', norm_text)
    return text  # Remove control characters
   

input_filename = 'full_dataset.csv'
output_filename = 'gathered.csv'


try:
    df = pd.read_csv(input_filename, encoding='utf-8-sig')
except FileNotFoundError:
    print("Error: input file was not found.")
    exit(1)

# Subset df by source == 'Gathered'
df = df[df['source'] == 'Gathered']


# Clean only string columns using clean_text function
for col in df.select_dtypes(include='object').columns:
    df[col] = df[col].apply(clean_text)

# Drop the first column if it's an unnamed index
if df.columns[0].startswith('Unnamed'):
    df = df.iloc[:, 1:]


df.to_csv(output_filename, index=False, encoding='utf-8')
print(f"Cleaned and filtered data has been written to {output_filename}")

# Print the number of lines in output_filename (including header)
print(f"Number of lines in {output_filename}: {sum(1 for _ in open(output_filename, encoding='utf-8'))}")


