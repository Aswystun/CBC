
# This script to analyze ingredient categories in the NER column of a recipe dataset
# And to reduce the number of synonyms by grouping them into broader categories


import pandas as pd
import ast
from collections import Counter



INPUT_FILENAME = 'gathered_short.csv'
# LINE_LIMIT = 100000



CATEGORIES = {
    "Meat": {"beef", "ground beef", "chuck", "hamburger", "meat", "lamb", "steak", "sirloin", },
    "Seasoning": {"salt", "pepper", "chili powder", "black pepper", "and pepper", "and pepper to taste", "garlic powder", "onion, chopped", "chopped onion", "onion", "garlic, minced"},
    "Dairy": {"milk", "sour cream", "butter", "cream of mushroom soup"},
    "Sauce": {"worcestershire sauce", "soy sauce", "ketchup"},
    "Oil": {"olive oil", "oil", "vegetable oil"},
    "Egg": {"eggs", "egg"},
    "Flour": {"flour"},
    "Water": {"water"},
    "Sour Cream": {"sour cream"},
    "Cornstarch": {"cornstarch"},
}  


def analyze_ner_ingredients():
    try:
      
        df = pd.read_csv(INPUT_FILENAME)  
        if 'NER' not in df.columns:
            print("❌ ERROR: 'NER' column not found in the header.")
            return

        # Prepare a counter for each category
        ingredient_counts = {category: Counter() for category in CATEGORIES}

        # Iterate through each recipe's NER list
        for ner_list_str in df['NER'].dropna():
            try:
                # Parse the NER column as a Python list
                ner_ingredients = ast.literal_eval(ner_list_str)
                if not isinstance(ner_ingredients, list):
                    print("  Skipping invalid NER entry (not a list):", ner_list_str)
                    continue
            except (ValueError, SyntaxError) as e:
                print(f"Skipping malformed NER entry: {ner_list_str} (Error: {e})")
                continue

            # For each ingredient, check if it matches a category keyword
            for ingredient in ner_ingredients:
                ingredient_lower = ingredient.lower()
                for category, keywords in CATEGORIES.items():
                    if any(keyword in ingredient_lower for keyword in keywords):
                        ingredient_counts[category][ingredient] += 1
                        break  # Only count an ingredient for the first matching category

        # Print a summary of the results
        print(f"\n--- Analysis Complete (scanned {len(df)} recipes) ---\n")
        print("Most common terms found in the NER column for each baking category:\n")
        for category, counts in ingredient_counts.items():
            print(f"--- {category} ---")
            if not counts:
                print("  (No terms found for this category in the sample)")
            else:
                for term, count in counts.most_common(10):
                    print(f"  - {term}: {count} times")
            print("-" * 20 + "\n")
    except FileNotFoundError:
        print(f"❌ ERROR: The file '{INPUT_FILENAME}' was not found.")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")


# Run the analysis if this script is executed directly
if __name__ == "__main__":
    analyze_ner_ingredients()




###########################
#                         #
#                         #
#         Results         #
#                         #
#                         #
###########################





# --- Analysis Complete (scanned 200000 recipes) ---
# 
# Most common terms found in the NER column for each baking category:
# 
# --- Meat ---
#   - ground beef: 6543 times
#   - hamburger: 1966 times
#   - beef: 1313 times
#   - beef broth: 1121 times
#   - lean ground beef: 957 times
#   - ground chuck: 558 times
#   - crabmeat: 477 times
#   - crab meat: 435 times
#   - beef stock: 371 times
#   - ground meat: 330 times
# --------------------
# 
# --- Seasoning ---
#   - salt: 84010 times
#   - onion: 36139 times
#   - pepper: 17562 times
#   - onions: 8455 times
#   - Salt: 6019 times
#   - green pepper: 6018 times
#   - black pepper: 5409 times
#   - green onions: 4979 times
#   - red pepper: 4303 times
#   - unsalted butter: 4168 times
# --------------------
# 
# --- Dairy ---
#   - butter: 45912 times
#   - milk: 33377 times
#   - sour cream: 11402 times
#   - buttermilk: 4483 times
#   - cream of mushroom soup: 3862 times
#   - peanut butter: 3646 times
#   - Butter: 3321 times
#   - condensed milk: 2118 times
#   - Milk: 1739 times
#   - coconut milk: 806 times
# --------------------
# 
# --- Sauce ---
#   - soy sauce: 5830 times
#   - Worcestershire sauce: 5775 times
#   - ketchup: 2317 times
#   - worcestershire sauce: 233 times
#   - Soy Sauce: 117 times
#   - tomato ketchup: 89 times
#   - Worcestershire Sauce: 81 times
#   - Ketchup: 57 times
#   - light soy sauce: 34 times
#   - Soy sauce: 31 times
# --------------------
# 
# --- Oil ---
#   - olive oil: 15833 times
#   - oil: 8115 times
#   - vegetable oil: 7599 times
#   - boiling water: 3517 times
#   - canola oil: 2324 times
#   - extra virgin olive oil: 1964 times
#   - extra-virgin olive oil: 1718 times
#   - cooking oil: 1517 times
#   - sesame oil: 1463 times
#   - salad oil: 1418 times
# --------------------
# 
# --- Egg ---
#   - eggs: 38907 times
#   - egg: 15262 times
#   - egg whites: 2951 times
#   - egg yolks: 2820 times
#   - Eggs: 1908 times
#   - Egg: 988 times
#   - egg yolk: 971 times
#   - egg noodles: 775 times
#   - eggplant: 615 times
#   - egg white: 319 times
# --------------------
# 
# --- Flour ---
#   - flour: 44421 times
#   - Flour: 1719 times
#   - whole wheat flour: 1268 times
#   - flour tortillas: 1050 times
#   - cake flour: 967 times
#   - bread flour: 491 times
#   - all-purpose flour: 301 times
#   - white flour: 222 times
#   - cornflour: 159 times
#   - Whole Wheat Flour: 153 times
# --------------------
# 
# --- Water ---
#   - water: 29559 times
#   - cold water: 2335 times
#   - Water: 1384 times
#   - water chestnuts: 1245 times
#   - warm water: 949 times
#   - hot water: 364 times
#   - watermelon: 126 times
#   - very warm water: 60 times
#   - watercress: 57 times
#   - sparkling water: 51 times
# --------------------
# 
# --- Sour Cream ---
#   (No terms found for this category in the sample)
# --------------------
# 
# --- Cornstarch ---
#   - cornstarch: 5407 times
#   - Cornstarch: 205 times
#   - cornstarch +: 3 times
#   - cornstarch roux: 2 times
#   - cornstarch]: 1 times
#   - TB cornstarch: 1 times
#   - cornstarch pudding: 1 times
#   - rounded cornstarch: 1 times
#   - CORNSTARCH: 1 times
#   - -Cornstarch: 1 times
# --------------------