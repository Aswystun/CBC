import streamlit as st
import pandas as pd
import plotly.express as px

# Load your CSV
df = pd.read_csv("parsed.csv")
# Ensure total_meat is always float
df['total_meat'] = pd.to_numeric(df['total_meat'], errors='coerce')
# Create a unique label for each recipe: title (link)
df['unique_label'] = df['title'] + ' (' + df['link'].astype(str) + ')'
# For display, keep just the title for x-axis
df['display_title'] = df['title']

st.title("Recipe Carbon Emissions Explorer 🌍")

# Search bar

search = st.text_input("Search for a recipe title:")

if search:
    results = df[df['title'].str.contains(search, case=False, na=False)]
else:
    results = df.copy()

# Show a few results
st.write(f"Found {len(results)} recipes matching.")

selected_labels = st.multiselect(
    "Select recipes to compare:",
    results['unique_label'].tolist()
)

# Show plot if any selected
if selected_labels:
    selected_df = results[results['unique_label'].isin(selected_labels)].copy()
    # For x-axis, use just the recipe title
    selected_df['display_title'] = selected_df['title']
    fig = px.bar(
        selected_df,
        x='display_title',
        y='total_meat',
        labels={'total_meat': 'kg CO₂e from meat'},
        title="Carbon Emissions from Meat per Recipe"
    )
    fig.update_layout(xaxis_title=None)  # Remove x-axis label
    st.plotly_chart(fig)

# Optional: Show recipe details
if 'selected_df' in locals() and st.checkbox("Show recipe ingredients and directions"):
    for _, row in selected_df.iterrows():
        st.subheader(f"{row['title']} ({row['link']})")
        st.markdown(f"**Total emissions:** {round(row['total_meat'], 2)} kg CO₂e")
        st.markdown("**Ingredients:**")
        st.write(eval(row['ingredients']))  # If it's a list stored as string
        st.markdown("**Directions:**")
        st.write(eval(row['directions']))