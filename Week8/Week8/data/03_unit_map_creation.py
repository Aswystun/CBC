# I am interested in red_meat dishes and would like to focus on recipes including red meat. 
# This script will help identify common units used in these recipes to create a unit_map for cleaning.
# I will be using the temp file /the subset of 200,000 rows 'gathered_short.csv' created earlier.

import pandas as pd
import re
from collections import Counter

# Load your subset
df = pd.read_csv('gathered_short.csv', encoding='utf-8')

# Define red meat keywords
red_meat_keywords = ['beef', 'steak', 'lamb', 'pork', 'veal', 'roast', 'ribs', 'brisket', 'chuck', 'sirloin']

# Words to ignore (units, descriptors)
ignore_words = {
    "c", "cup", "cups", "tsp", "teaspoon", "teaspoons", "tbsp", "tablespoon", "tablespoons",
    "oz", "ounce", "ounces", "lb", "lbs", "pound", "pounds", "can", "cans", "pkg", "pkgs",
    "large", "small", "medium", "slices", "slice", "to", "of"
}

# Filter for recipes with red meat in the NER column (case-insensitive)
mask = df['NER'].str.lower().str.contains('|'.join(red_meat_keywords), na=False)
red_meat_df = df[mask]

ingredient_pattern = re.compile(r'["\']([^"\']+)["\']')  # For list-like stringified ingredients
ingredient_counter = Counter()

for ingredients in red_meat_df['ingredients']:
    try:
        items = ingredient_pattern.findall(ingredients)
        for item in items:
            # Remove quantity and unit at the start (e.g., "1 lb. ground beef" -> "ground beef")
            name = re.sub(r'^([\d\s/\.-]+)?([a-zA-Z]+\.?\s+)?', '', item).strip().lower()
            # Remove any remaining unit words at the start
            name = re.sub(r'^(%s)\s+' % '|'.join(ignore_words), '', name)
            # Only count if not a unit/descriptor and not empty
            if name and name not in ignore_words:
                ingredient_counter[name] += 1
    except Exception:
        continue

# Show the most common ingredient names (top 30)
print('Suggested CATEGORIES = {')
for name, count in ingredient_counter.most_common(30):
    print(f'    "{name}": {count},')
print('}')




# Suggested CATEGORIES = {
#    "salt": 7255,
#    "ground beef": 5375,
#    ",": 4160,
#    "pepper": 4127,
#    "water": 3837,
#    "onion, chopped": 2539,
#    "worcestershire sauce": 1916,
#    "olive oil": 1775,
#    "chopped onion": 1726,
#    "brown sugar": 1536,
#    "sugar": 1519,
#    "chili powder": 1493,
#    "milk": 1474,
#    "butter": 1457,
#    "flour": 1317,
#    "soy sauce": 1288,
#    "onion": 1258,
#    "garlic powder": 1121,
#    "oil": 1030,
#    "ketchup": 1003,
#    "eggs": 1003,
#    "and pepper": 973,
#    "vegetable oil": 942,
#    "lean ground beef": 933,
#    "egg": 933,
#    "garlic, minced": 922,
#    "black pepper": 921,
#    "sour cream": 883,
#    "and pepper to taste": 875,
#    "cornstarch": 793,
#}
