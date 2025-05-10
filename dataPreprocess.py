import pandas as pd
import re

# Load the dataset
df = pd.read_csv("dataset/recipes.csv")

# Drop rows with missing recipe name or ingredients
df = df.dropna(subset=['recipe_name', 'ingredients'])

# Remove duplicates
df = df.drop_duplicates()


def clean_text(text):
    text = text.lower()                           # lowercase
    text = re.sub(r'\[.*?\]|\(.*?\)', '', text)   # remove brackets
    text = re.sub(r'[^a-zA-Z, ]', '', text)       # remove punctuation except commas
    text = re.sub(r'\s+', ' ', text)              # normalize spaces
    return text.strip()

# Apply cleaning
df['recipe_name'] = df['recipe_name'].apply(clean_text)
df['ingredients'] = df['ingredients'].apply(clean_text)


#Convert ingredients to list for better manipulation
df['ingredients_list'] = df['ingredients'].apply(lambda x: [i.strip() for i in x.split(',') if i.strip()])



#show recipe names and ingredients after data cleaning
recipes = df[['recipe_name', 'ingredients']].dropna()
counter = 0
for index, row in recipes.iterrows():
    print(f"Recipe: {row['recipe_name']}")
    print(f"Ingredients: {row['ingredients']}\n")

