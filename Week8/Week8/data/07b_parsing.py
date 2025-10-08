import pandas as pd
import ast
import re

# Load the cleaned recipe data
df = pd.read_csv('gathered_refined.csv')

# Load the emissions data
emissions = pd.read_csv('emissions.csv')

# Map ingredient keywords to emissions entities
ingredient_to_entity = {
    'ground beef': 'Beef (beef herd)',
    'beef': 'Beef (beef herd)',
    'hamburger': 'Beef (beef herd)',
    'chuck': 'Beef (beef herd)',
    'sirloin': 'Beef (beef herd)',
    'steak': 'Beef (beef herd)',
    'lamb': 'Lamb & Mutton',
    'mutton': 'Lamb & Mutton',
    'pork': 'Pig Meat',
    'turkey': 'Poultry Meat',
}

# Exclude these keywords from ingredient lines (e.g., broths, stocks, extracts)
exclude_keywords = ['broth', 'stock', 'extract']
# Volume units to skip for meat emissions
volume_units = ['cup', 'cups', 'ml', 'l', 'liter', 'litre', 'liters', 'litres', 'quart', 'quarts', 'pint', 'pints', 'gallon', 'gallons', 'fluid', 'fl', 'oz']

def get_emissions(entity):
    row = emissions[emissions['Entity'] == entity]
    if not row.empty:
        return row.iloc[0]['total']
    return 0

def to_kg(amount, unit):
    unit = unit.lower()
    if unit in ['g', 'gram', 'grams']:
        return amount / 1000
    if unit in ['kg', 'kilogram', 'kilograms']:
        return amount
    if unit in ['mg', 'milligram', 'milligrams']:
        return amount / 1e6
    if unit in ['lb', 'lbs', 'pound', 'pounds']:
        return amount * 0.453592
    if unit in ['oz', 'ounce', 'ounces']:
        return amount * 0.0283495
    # fallback: assume already kg
    return amount

def extract_best_amount_unit(line):
    # Find all number+unit pairs, including fractions like 1 1/2
    # This regex matches numbers like 1, 1.5, 1,5, 1 1/2, 2/3, etc.
    matches = re.findall(r'(\d+\s+\d+/\d+|\d+/\d+|\d+[\.,]?\d*)\s*([a-zA-Z]+)', line)
    best_amt = None
    best_unit = None
    max_amt = 0
    for amt_str, unit in matches:
        # Convert mixed fractions like '1 1/2' to float
        if ' ' in amt_str:
            whole, frac = amt_str.split()
            num, denom = frac.split('/')
            amt = float(whole) + float(num) / float(denom)
        elif '/' in amt_str:
            num, denom = amt_str.split('/')
            amt = float(num) / float(denom)
        else:
            amt = float(amt_str.replace(',', '.'))
        # Prefer the largest amount (e.g., 6 lbs over 1 lb)
        if amt > max_amt:
            max_amt = amt
            best_amt = amt
            best_unit = unit
    return best_amt, best_unit

results = []
for idx, row in df.iterrows():
    total_meat = 0
    try:
        ner = ast.literal_eval(row['NER'])
    except Exception as e:
        print(f"Row {idx} NER parse error: {e}")
        ner = []
    for ent in ner:
        text = ent.lower() if isinstance(ent, str) else str(ent).lower()
        matched = None
        for k, v in ingredient_to_entity.items():
            if k in text:
                matched = v
                break
        if matched:
            try:
                ingredients_list = ast.literal_eval(row['ingredients'])
            except Exception as e:
                print(f"Row {idx} ingredients parse error: {e}")
                ingredients_list = []
            best_line = None
            for ing_line in ingredients_list:
                ing_line_l = ing_line.lower()
                if text in ing_line_l:
                    # Exclude broths, stocks, extracts
                    if any(ex in ing_line_l for ex in exclude_keywords):
                        print(f"Row {idx}: skipping excluded ingredient line: '{ing_line}'")
                        continue
                    best_line = ing_line
                    break
            if best_line:
                print(f"Row {idx}: matched '{k}' in '{text}' to entity '{matched}'")
                print(f"  Matched full ingredient line: '{best_line}'")
                amt, unit = extract_best_amount_unit(best_line)
                if amt is not None and unit is not None:
                    # Skip volume units
                    if unit.lower() in volume_units:
                        print(f"    Skipping volume unit '{unit}' in '{best_line}'")
                        continue
                    kg = to_kg(amt, unit)
                    emis = get_emissions(matched)
                    print(f"    Extracted: amt={amt}, unit={unit}, kg={kg}, emis={emis}")
                    total_meat += kg * emis
                else:
                    print(f"    Could not extract amount/unit from '{best_line}'")
            else:
                print(f"  Could not find matching ingredient line for '{text}' in recipe.")
        else:
            for k in ingredient_to_entity:
                if k in text:
                    print(f"Row {idx}: found '{k}' in '{text}' but no match (check regex)")
    print(f"Row {idx}: total_meat={total_meat}")
    results.append(total_meat)
df['total_meat'] = results
df.to_csv('parsed_test.csv', index=False)
