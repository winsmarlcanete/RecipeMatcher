from dataPreprocess import clean_recipe_data

df = clean_recipe_data("dataset/recipes.csv")

# Display the cleaned recipe names and ingredients
for index, row in df[['recipe_name', 'ingredients']].iterrows():
    print(f"Recipe: {row['recipe_name']}")
    print(f"Ingredients: {row['ingredients']}\n")