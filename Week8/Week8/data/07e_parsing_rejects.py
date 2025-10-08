import pandas as pd

# Load the rejects.csv file
df = pd.read_csv('rejects.csv')

# Extract only the 'ingredients' and 'rejection_reason' columns
reasons = df[['ingredients', 'rejection_reason']].copy()

# Save to reject_reasons.csv
reasons.to_csv('reject_reasons.csv', index=False)


# created 'reject_reasons.csv' which will be used to improve parsing in 07f_parsing.py