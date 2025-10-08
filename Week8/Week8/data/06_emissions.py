import pandas as pd

# Fetch the data.
df = pd.read_csv("https://ourworldindata.org/grapher/food-emissions-supply-chain.csv?v=1&csvType=full&useColumnShortNames=true", storage_options = {'User-Agent': 'Our World In Data data fetch/1.0'})

df.to_csv("emissions.csv", index=False)

# Calculate total emissions by summing the relevant columns for each row
emission_cols = [
	'food_emissions_land_use',
	'food_emissions_farm',
	'food_emissions_animal_feed',
	'food_emissions_processing',
	'food_emissions_transport',
	'food_emissions_retail',
	'food_emissions_packaging',
	'food_emissions_losses'
]
df['total'] = df[emission_cols].sum(axis=1)

# Save to a local CSV file with the new 'total' column
df.to_csv("emissions.csv", index=False)
print("Saved emissions.csv")


# Print the header (column names) and first 5 rows of the downloaded CSV
print("Header of emissions.csv:")
print(list(df.columns))
print("\nFirst 5 rows:")
print(df.head())

