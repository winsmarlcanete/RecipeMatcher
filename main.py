from dataPreprocess import clean_recipe_data
from recommendersAlgorithm import string_match_recommender, brute_force_recommender, greedy_recommender

df = clean_recipe_data("dataset/recipes.csv")
user_ingredients = ['egg', 'flour', 'milk']

print("=== String Match ===")
print(string_match_recommender(df, user_ingredients))

print("\n=== Brute Force ===")
print(brute_force_recommender(df, user_ingredients))

print("\n=== Greedy Match ===")
print(greedy_recommender(df, user_ingredients))

