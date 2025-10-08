
# This script will test our subset for hidden character issues, written by Dr. Goertzen

import csv
import unicodedata
from collections import Counter

# --- Configuration ---
# Set the file to analyze and how many lines to check.
FILENAME = 'gathered_short.csv'
LINES_TO_CHECK = 50000


def analyze_file_integrity():
    """
    Reads the start of a CSV and reports on potential character issues.
    """
    print(f"--- Starting analysis of '{FILENAME}' (up to {LINES_TO_CHECK} lines) ---")

    # 1. First, check for a BOM by reading the first few bytes of the file.
    try:
        with open(FILENAME, 'rb') as f:
            if f.read(3) == b'\xef\xbb\xbf':
                print("✅ File Encoding: UTF-8 with a Byte Order Mark (BOM) detected.")
            else:
                print("ℹ️ File Encoding: No UTF-8 BOM detected at the start of the file.")
    except FileNotFoundError:
        print(f"❌ ERROR: The file '{FILENAME}' was not found.")
        return

    # Data structures to hold our findings.
    control_char_counts = Counter()
    locations = []
    MAX_EXAMPLES = 10
    lines_processed = 0

    try:
        # 2. Now, read the file as text to check content.
        # We use 'utf-8' here on purpose to catch errors. The cleaning script
        # will use 'utf-8-sig' to handle the BOM it finds.
        with open(FILENAME, 'r', encoding='utf-8', newline='') as f:
            reader = csv.reader(f)
            for line_num, row in enumerate(reader, 1):
                if line_num > LINES_TO_CHECK:
                    break
                
                # Check each cell in the row for problematic characters.
                for col_num, cell in enumerate(row):
                    for char in cell:
                        # 'unicodedata.category(char).startswith('C')' is a robust
                        # way to identify all standard control characters.
                        if unicodedata.category(char).startswith('C'):
                            control_char_counts[char] += 1
                            if len(locations) < MAX_EXAMPLES:
                                # Save details of the first few occurrences.
                                locations.append({
                                    'line': line_num,
                                    'col': col_num,
                                    'char': repr(char), # repr() makes invisible chars visible
                                    'context': cell[:70]
                                })
                lines_processed = line_num

    except UnicodeDecodeError as e:
        print(f"\n❌ CRITICAL ERROR: File is not valid UTF-8.")
        print(f"   Analysis stopped because a character could not be decoded.")
        print(f"   Details: {e}")
        return
    except Exception as e:
        print(f"\n❌ An unexpected error occurred during processing: {e}")
        return

    # 3. Finally, print a summary of the findings.
    print(f"\n--- Analysis Complete (scanned {lines_processed} lines) ---")
    if not control_char_counts:
        print("✅ Success! No problematic control characters were found.")
    else:
        print(f"⚠️ Found {len(control_char_counts)} types of hidden control characters:")
        for char, count in control_char_counts.items():
            print(f"   - Character: {repr(char)}, Count: {count}")
        
        print("\nHere are the first few examples of where they were found:")
        for loc in locations:
            print(f"   - Line {loc['line']}, Col {loc['col']}: Found {loc['char']} in text starting with: '{loc['context']}'")

# --- Run the Analysis ---
if __name__ == "__main__":
    analyze_file_integrity()

