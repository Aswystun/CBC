
# The objective of this script is to clean and normalize the ingredients and directions for recipes
import pandas as pd
import re
import ast


def normalize_units(text):
    words = text.split()
    normalized = [unit_map.get(w, w) for w in words]
    return ' '.join(normalized)

def clean_item(text):
    text = text.lower()
    # Allow spaces, /, ., (, and )
    text = re.sub(r'[^a-zA-Z0-9\s/\.\(\)]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    text = normalize_units(text)
    return text


def clean_list_column(cell):
    try:
        items = ast.literal_eval(cell)
        if isinstance(items, list):
            cleaned = [clean_item(i) for i in items]
            return str(cleaned)
    except Exception as e:
        print(f"Error processing cell: {cell}, Error: {e}")
    return clean_item(cell)


# Read the dataset
df = pd.read_csv('gathered_short.csv', encoding='utf-8')


# Clean ingredients
if 'ingredients' in df.columns:
    df['ingredients'] = df['ingredients'].apply(clean_list_column)

# Clean directions
if 'directions' in df.columns:
    df['directions'] = df['directions'].apply(clean_list_column)



# Save the dataframe with cleaned columns
df.to_csv('gathered_short_cleaned.csv', index=False, encoding='utf-8')
print("Cleaned data saved to 'gathered_short_cleaned.csv'")

# Print the number of rows
with open('gathered_short_cleaned.csv', encoding='utf-8') as f:
    row_count = sum(1 for _ in f) - 1


# The result was a new .csv 'gathered_short_cleaned.csv' with 10,000 rows.