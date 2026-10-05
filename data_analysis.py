import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('All_Diets.csv')

df.fillna(df.mean(numeric_only=True), inplace=True)

avg_macros = df.groupby('Diet_type')[['Protein(g)', 'Carbs(g)', 'Fat(g)']].mean()
print("--- Average Macronutrients per Diet ---")
print(avg_macros)

top_protein = df.sort_values('Protein(g)', ascending=False).groupby('Diet_type').head(5)
print("\n--- Top 5 Protein-Rich Recipes per Diet ---")
print(top_protein[['Diet_type', 'Recipe_name', 'Protein(g)']])

highest_protein_diet = avg_macros['Protein(g)'].idxmax()
print(f"\n--- Diet with Highest Average Protein: {highest_protein_diet} ---")

common_cuisines = df.groupby(['Diet_type', 'Cuisine_type']).size().reset_index(name='count')
common_cuisines = common_cuisines.sort_values(['Diet_type', 'count'], ascending=[True, False]).drop_duplicates('Diet_type')
print("\n--- Most Common Cuisine per Diet ---")
print(common_cuisines[['Diet_type', 'Cuisine_type', 'count']])

df['Protein_to_Carbs_ratio'] = df['Protein(g)'] / (df['Carbs(g)'] + 1e-9)
df['Carbs_to_Fat_ratio'] = df['Carbs(g)'] / (df['Fat(g)'] + 1e-9)

sns.set_theme(style="whitegrid")

plt.figure(figsize=(10, 6))
avg_macros.plot(kind='bar', figsize=(12, 6))
plt.title('Average Macronutrient Content by Diet Type')
plt.ylabel('Grams (g)')
plt.xlabel('Diet Type')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('avg_macros_bar_chart.png')
plt.show()

plt.figure(figsize=(8, 6))
sns.heatmap(avg_macros, annot=True, cmap='YlGnBu', fmt=".1f")
plt.title('Heatmap of Macronutrients by Diet Type')
plt.tight_layout()
plt.savefig('macros_heatmap.png')
plt.show()

plt.figure(figsize=(10, 6))
sns.scatterplot(data=top_protein, x='Protein(g)', y='Cuisine_type', hue='Diet_type', s=100)
plt.title('Top 5 Protein-Rich Recipes by Cuisine and Diet')
plt.tight_layout()
plt.savefig('top_protein_scatter.png')
plt.show()