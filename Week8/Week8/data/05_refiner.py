import pandas as pd
import ast

input_filename = 'gathered_short.csv'
output_filename = 'gathered_refined.csv' 

CATEGORIES = {
    "Meat": ( {"beef", "ground beef", "chuck", "hamburger", "meat", "lamb", "steak", "sirloin",}, {"crab"} ),
    "Seasoning": ( {"salt", "pepper", "chili powder", "black pepper", "and pepper", "and pepper to taste", "garlic powder", "onion, chopped", "chopped onion", "onion", "garlic, minced",}, {"butter"} ),
    "Dairy": ( {"milk", "sour cream", "butter", "cream of mushroom soup",}, {"peanut","coconut"} ),
    "Sauce": ( {"worcestershire sauce", "soy sauce", "ketchup"}, set() ),
    "Oil": ( {"olive oil", "oil", "vegetable oil",}, {"water"} ),
    "Egg": ( {"eggs", "egg",}, {"plant"} ),
    "Flour": ( {"flour"}, set() ),
    "Water": ( {"water",}, {"chestnuts", "melon"} ),
    "Cornstarch": ( {"cornstarch",}, {"pudding"} ),
}

#only include recipes that match the "Meat" category as criteria
def matches_meat_category(ner_list):
    include, exclude = CATEGORIES["Meat"]
    for ingredient in ner_list:
        ingredient_lower = ingredient.lower()
        if any(ex in ingredient_lower for ex in exclude):
            continue
        if any(keyword in ingredient_lower for keyword in include):
            return True
    return False

df = pd.read_csv(input_filename, encoding='utf-8')
mask = []

for ner_str in df['NER']:
    try:
        ner_list = ast.literal_eval(ner_str)
        if isinstance(ner_list, list) and matches_meat_category(ner_list):
            mask.append(True)
        else:
            mask.append(False)
    except Exception:
        mask.append(False)

df_refined = df[mask]
df_refined.to_csv(output_filename, index=False, encoding='utf-8')

# Print the number of lines (including header)
with open(output_filename, encoding='utf-8') as f:
    line_count = sum(1 for _ in f)
print(f"Number of lines in {output_filename}: {line_count}")


###########################
#                         #
#                         #
#         Results         #
#                         #
#                         #
###########################


# Number of lines in gathered_refined.csv: 18959
