import pandas as pd

# Read the filtered data
df = pd.read_csv('gathered.csv', encoding='utf-8')

# Take a random sample of 200,000 rows (or all rows if fewer)
sample_size = min(200000, len(df))
df_sample = df.sample(n=sample_size, random_state=42)

# Save to new CSV
df_sample.to_csv('gathered_short.csv', index=False, encoding='utf-8')
print(f"Saved {sample_size} random rows to gathered_short.csv")
