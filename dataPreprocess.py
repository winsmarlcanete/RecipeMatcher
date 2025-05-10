import pandas as pd
import re

def clean_recipe_data(csv_path):
    # Load the dataset
    df = pd.read_csv(csv_path)

    # Drop rows with missing recipe name or ingredients
    df = df.dropna(subset=['recipe_name', 'ingredients'])

    # Remove duplicates
    df = df.drop_duplicates()

    # Text cleaning function
    def clean_text(text):
        text = text.lower()                           # lowercase
        text = re.sub(r'\[.*?\]|\(.*?\)', '', text)   # remove brackets
        text = re.sub(r'[^a-zA-Z, ]', '', text)       # remove punctuation except commas
        text = re.sub(r'\s+', ' ', text)              # normalize spaces
        return text.strip()

    # Apply cleaning
    df['recipe_name'] = df['recipe_name'].apply(clean_text)
    df['ingredients'] = df['ingredients'].apply(clean_text)

    # Convert ingredients to list for easier matching
    df['ingredients_list'] = df['ingredients'].apply(
        lambda x: [i.strip() for i in x.split(',') if i.strip()]
    )

    return df


