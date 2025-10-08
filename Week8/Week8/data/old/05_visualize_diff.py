import csv

# File paths
original_file = 'Gathered_short.csv'
cleaned_file = 'Gathered_short_cleaned.csv'
diff_file = 'diff_report.txt'

# Read both files
with open(original_file, encoding='utf-8') as f1, open(cleaned_file, encoding='utf-8') as f2:
	reader1 = list(csv.reader(f1))  # Original file rows
	reader2 = list(csv.reader(f2))  # Cleaned file rows

# Separate headers and data rows for both files
header1 = reader1[0]
header2 = reader2[0]
rows1 = reader1[1:]
rows2 = reader2[1:]

with open(diff_file, 'w', encoding='utf-8') as out:
	# Write a header for the diff report
	out.write('# Differences between Gathered_short.csv and Gathered_short_cleaned.csv\n')
	out.write(f'# Columns: {header1}\n\n')
	# Compare each row by index; if different, write both versions
	for idx, (row1, row2) in enumerate(zip(rows1, rows2), 1):
		if row1 != row2:
			out.write(f'# original line {idx}:\n')
			out.write(','.join(row1) + '\n')
			out.write(f'# new line after change {idx}:\n')
			out.write(','.join(row2) + '\n\n')
	# If files have different lengths, note extra lines
	if len(rows1) != len(rows2):
		out.write(f'# File lengths differ: {len(rows1)} vs {len(rows2)} rows.\n')
		if len(rows1) > len(rows2):
			# Write extra lines from the original file
			for idx, row1 in enumerate(rows1[len(rows2):], len(rows2)+1):
				out.write(f'# original line {idx}:\n')
				out.write(','.join(row1) + '\n')
				out.write(f'# new line after change {idx}:\n')
				out.write('[NO LINE]\n\n')
		else:
			# Write extra lines from the cleaned file
			for idx, row2 in enumerate(rows2[len(rows1):], len(rows1)+1):
				out.write(f'# original line {idx}:\n')
				out.write('[NO LINE]\n')
				out.write(f'# new line after change {idx}:\n')
				out.write(','.join(row2) + '\n\n')
# Print confirmation to the console
print(f'Diff report written to {diff_file}')
