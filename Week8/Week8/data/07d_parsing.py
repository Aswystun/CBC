import pandas as pd
import ast
import re

# Load the cleaned recipe data
df = pd.read_csv('gathered_refined.csv')

# Load the emissions data
emissions = pd.read_csv('emissions.csv')

# Map ingredient keywords to emissions entities (expanded for generic/ambiguous terms)
# I might be missing a lot, so including popular terms from 03b script.

# I initially tested it with more terms from 03b script, but no change, so adding rejection reasons for manual review


ingredient_to_entity = {
    'ground beef': 'Beef (beef herd)',
    'lean ground beef': 'Beef (beef herd)',
    'beef': 'Beef (beef herd)',
    'steak': 'Beef (beef herd)',
    'hamburger': 'Beef (beef herd)',
    'hamburger meat': 'Beef (beef herd)',
    'chuck': 'Beef (beef herd)',
    'chuck steak': 'Beef (beef herd)',
    'ground chuck': 'Beef (beef herd)',
    'sirloin': 'Beef (beef herd)',
    'steak': 'Beef (beef herd)',
    'round steak': 'Beef (beef herd)',
    'lamb': 'Lamb & Mutton',
    'ground lamb': 'Lamb & Mutton',
    'mutton': 'Lamb & Mutton',
    'pork': 'Pig Meat',
    'pork sausage': 'Pig Meat',
    'pork tenderloin': 'Pig Meat',
    'bulk pork sausage': 'Pig Meat',
    'ground pork': 'Pig Meat',
    'turkey': 'Poultry Meat',
}

# Exclude these keywords from ingredient lines (e.g., broths, stocks, extracts)
exclude_keywords = ['broth', 'stock', 'extract']
# Volume units to skip for meat emissions
volume_units = ['cup', 'cups', 'ml', 'l', 'liter', 'litre', 'liters', 'litres', 'quart', 'quarts', 'pint', 'pints', 'gallon', 'gallons', 'fluid', 'fl', 'oz']

# For ambiguous terms, collect for manual review
def is_ambiguous(text):
    ambiguous_terms = ['meat', 'ground meat']
    return any(term in text for term in ambiguous_terms)

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
    matches = re.findall(r'(\d+\s+\d+/\d+|\d+/\d+|\d+[\.,]?\d*)\s*([a-zA-Z]+)', line)
    best_amt = None
    best_unit = None
    max_amt = 0
    for amt_str, unit in matches:
        if ' ' in amt_str:
            whole, frac = amt_str.split()
            num, denom = frac.split('/')
            amt = float(whole) + float(num) / float(denom)
        elif '/' in amt_str:
            num, denom = amt_str.split('/')
            amt = float(num) / float(denom)
        else:
            amt = float(amt_str.replace(',', '.'))
        if amt > max_amt:
            max_amt = amt
            best_amt = amt
            best_unit = unit
    return best_amt, best_unit

results = []
ambiguous_rows = []
rejection_reasons = []
for idx, row in df.iterrows():
    total_meat = 0
    rejection_reason = []
    try:
        ner = ast.literal_eval(row['NER'])
    except Exception as e:
        print(f"Row {idx} NER parse error: {e}")
        ner = []
        rejection_reason.append(f"NER parse error: {e}")
    found_meat = False
    for ent in ner:
        text = ent.lower() if isinstance(ent, str) else str(ent).lower()
        matched = None
        for k, v in ingredient_to_entity.items():
            if k in text:
                matched = v
                break
        if matched:
            found_meat = True
            try:
                ingredients_list = ast.literal_eval(row['ingredients'])
            except Exception as e:
                print(f"Row {idx} ingredients parse error: {e}")
                ingredients_list = []
                rejection_reason.append(f"ingredients parse error: {e}")
            best_line = None
            for ing_line in ingredients_list:
                ing_line_l = ing_line.lower()
                if text in ing_line_l:
                    if any(ex in ing_line_l for ex in exclude_keywords):
                        print(f"Row {idx}: skipping excluded ingredient line: '{ing_line}'")
                        rejection_reason.append(f"excluded keyword in '{ing_line}'")
                        continue
                    best_line = ing_line
                    break
            if best_line:
                print(f"Row {idx}: matched '{k}' in '{text}' to entity '{matched}'")
                print(f"  Matched full ingredient line: '{best_line}'")
                amt, unit = extract_best_amount_unit(best_line)
                if amt is not None and unit is not None:
                    if unit.lower() in volume_units:
                        print(f"    Skipping volume unit '{unit}' in '{best_line}'")
                        rejection_reason.append(f"volume unit '{unit}' in '{best_line}'")
                        continue
                    kg = to_kg(amt, unit)
                    emis = get_emissions(matched)
                    print(f"    Extracted: amt={amt}, unit={unit}, kg={kg}, emis={emis}")
                    total_meat += kg * emis
                else:
                    print(f"    Could not extract amount/unit from '{best_line}'")
                    rejection_reason.append(f"could not extract amount/unit from '{best_line}'")
                if is_ambiguous(text):
                    ambiguous_rows.append(row)
            else:
                print(f"  Could not find matching ingredient line for '{text}' in recipe.")
                rejection_reason.append(f"could not find matching ingredient line for '{text}'")
        else:
            for k in ingredient_to_entity:
                if k in text:
                    print(f"Row {idx}: found '{k}' in '{text}' but no match (check regex)")
                    rejection_reason.append(f"found '{k}' in '{text}' but no match")
    if not found_meat:
        rejection_reason.append("no mapped meat entity found in NER")
    print(f"Row {idx}: total_meat={total_meat}")
    results.append(total_meat)
    rejection_reasons.append('; '.join(rejection_reason))
df['total_meat'] = results
df['rejection_reason'] = rejection_reasons
# Output recipes with total_meat > 0 to parsed_test.csv
df_nonzero = df[df['total_meat'] > 0].copy()
df_nonzero.to_csv('parsed_test.csv', index=False)
# Output recipes with total_meat == 0 to rejects.csv, with rejection reason
df_zero = df[df['total_meat'] == 0].copy()
df_zero.to_csv('rejects.csv', index=False)
# Output ambiguous rows for manual review
df_ambiguous = pd.DataFrame(ambiguous_rows)
df_ambiguous.to_csv('ambiguous.csv', index=False)
print(f"Number of recipes in rejects.csv: {len(df_zero)}")
print(f"Number of ambiguous recipes in ambiguous.csv: {len(df_ambiguous)}")



# Results for this
# Number of recipes in rejects.csv: 3059
# Number of ambiguous recipes in ambiguous.csv: 292



