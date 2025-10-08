# This b script is based on the first script, but focuses on the red meat ingredients, 
# not just the most common ingredients from recipes including those red meat keywords.

import pandas as pd
import re
from collections import Counter

# Load your subset
df = pd.read_csv('gathered_short.csv', encoding='utf-8')

# Define red meat keywords
red_meat_keywords = ['beef', 'steak', 'lamb', 'pork', 'roast', 'ribs', 'brisket', 'chuck', 'sirloin', 'NY strip', 'tenderloin', 'filet', 'ground beef', 'hamburger']

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

# Only count ingredients that contain a red meat keyword
for ingredients in red_meat_df['ingredients']:
    try:
        items = ingredient_pattern.findall(ingredients)
        for item in items:
            # Remove quantity and unit at the start (e.g., "1 lb. ground beef" -> "ground beef")
            name = re.sub(r'^([\d\s/\.-]+)?([a-zA-Z]+\.?\s+)?', '', item).strip().lower()
            # Remove any remaining unit words at the start
            name = re.sub(r'^(%s)\s+' % '|'.join(ignore_words), '', name)
            # Only count if it contains a red meat keyword
            if name and any(meat in name for meat in red_meat_keywords):
                ingredient_counter[name] += 1
    except Exception:
        continue

# Show the most common red meat ingredient names (top 30)
print('Most common red meat ingredients in NER:')
for name, count in ingredient_counter.most_common(30):
    print(f'    "{name}": {count},')





# Most common red meat ingredients in NER:
#     "ground beef": 5375,
#     "hamburger": 1286,
#     "lean ground beef": 933,
#     "beef broth": 634,
#     "ground pork": 478,
#     "ground chuck": 476,
#     "beef stock": 295,
#     "pork and beans": 268,
#     "hamburger meat": 247,
#     "beef bouillon": 159,
#     "pork sausage": 157,
#     "ground lamb": 123,
#     "bulk pork sausage": 108,
#     "beef": 108,
#     "steak sauce": 105,
#     "pork tenderloin": 101,
#     "pork chops": 96,
#     "lean ground beef (90% lean)": 92,
#     "corned beef": 87,
#     "steak": 81,
#     "extra lean ground beef": 75,
#     "beef consomme": 75,
#     "beef bouillon granules": 71,
#     "ground beef, browned": 71,
#     "ground beef, browned and drained": 69,
#     "round steak": 68,
#     "beef stew meat": 67,
#     "pork": 66,
#     "ground sirloin": 65,
#     "dried beef": 58,