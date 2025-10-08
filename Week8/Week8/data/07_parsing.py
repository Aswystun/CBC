
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

# Helper: get emissions per kg for an entity
def get_emissions(entity):
    row = emissions[emissions['Entity'] == entity]
    if not row.empty:
        return row.iloc[0]['total']
    return 0

# Helper: normalize units to kg
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

# Main: parse each recipe
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
        # Try to match any red meat keyword in the text
        matched = None
        for k, v in ingredient_to_entity.items():
            # Use substring match for all keys for robustness
            if k in text:
                matched = v
                break
        if matched:
            print(f"Row {idx}: matched '{k}' in '{text}' to entity '{matched}'")
            # Now search for the best-matching full ingredient line
            try:
                ingredients_list = ast.literal_eval(row['ingredients'])
            except Exception as e:
                print(f"Row {idx} ingredients parse error: {e}")
                ingredients_list = []
            best_line = None
            for ing_line in ingredients_list:
                if text in ing_line.lower():
                    best_line = ing_line
                    break
            if best_line:
                print(f"  Matched full ingredient line: '{best_line}'")
                # Try to extract amount and unit from the full ingredient line
                m = re.search(r'(\d+[\.,]?\d*)\s*([a-zA-Z]+)', best_line)
                if m:
                    amt = float(m.group(1).replace(',', '.'))
                    unit = m.group(2)
                    kg = to_kg(amt, unit)
                    emis = get_emissions(matched)
                    print(f"    Extracted: amt={amt}, unit={unit}, kg={kg}, emis={emis}")
                    total_meat += kg * emis
                else:
                    print(f"    Could not extract amount/unit from '{best_line}'")
            else:
                print(f"  Could not find matching ingredient line for '{text}' in recipe.")
        else:
            # Only print if the text contains a known meat word (for debug)
            for k in ingredient_to_entity:
                if k in text:
                    print(f"Row {idx}: found '{k}' in '{text}' but no match (check regex)")
    print(f"Row {idx}: total_meat={total_meat}")
    results.append(total_meat)
df['total_meat'] = results
df.to_csv('parsed_test.csv', index=False)