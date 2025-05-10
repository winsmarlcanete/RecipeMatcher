import pandas as pd

# Load the dataset
df = pd.read_csv("dataset/recipes.csv")

#show recipe names and ingredients
recipes = df[['recipe_name', 'ingredients']].dropna()
counter = 0
for index, row in recipes.iterrows():
    print(f"Recipe: {row['recipe_name']}")
    print(f"Ingredients: {row['ingredients']}\n")
