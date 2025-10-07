import pandas as pd

# Read the cleaned dataset from the same directory as this script
df = pd.read_csv('full_dataset_cleaned.csv', encoding='utf-8')

# Filter rows where source == 'Gathered'
filtered = df[df['source'] == 'Gathered']

# Save the filtered DataFrame to a new CSV file
filtered.to_csv('Cleaned_Gathered.csv', index=False, encoding='utf-8')
print("Filtered data saved to 'Cleaned_Gathered.csv'")

# Print the number of lines in Cleaned_Gathered.csv (including header)
print(f"Number of lines in Cleaned_Gathered.csv: {sum(1 for _ in open('Cleaned_Gathered.csv', encoding='utf-8'))}")

# Number of lines in Cleaned_Gathered.csv: 1643099 

# Next develop a question for an analysis... 