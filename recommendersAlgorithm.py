# Function for string match algorithm
def string_match_recommender(df, user_ingredients, top_n=5):
    user_ingredients = [i.lower().strip() for i in user_ingredients]

    df['match_score'] = df['ingredients_list'].apply(
        lambda ingredients: (len(set(ingredients).intersection(user_ingredients)) / len(ingredients)) * 100
    )

    top_matches = df[df['match_score'] > 0].sort_values(by='match_score', ascending=False).head(top_n)

    # Convert to a list of dictionaries
    results = [{"name": row['recipe_name'], "score": row['match_score']} for _, row in top_matches.iterrows()]

    return results


# Function for brute force algorithm
def brute_force_recommender(df, user_ingredients, top_n=5, verbose=True):
    user_ingredients = [i.lower().strip() for i in user_ingredients]

    def percent_match(ingredients, available):
        return (sum(1 for item in ingredients if item in available) / len(ingredients)) * 100

    df['match_score'] = df['ingredients_list'].apply(
        lambda ingredients: percent_match(ingredients, user_ingredients)
    )

    matched_df = df[df['match_score'] > 0].sort_values(by='match_score', ascending=False)

    # Print verbose output if needed
    if verbose:
        print("\nTop Brute Force Matches:")
        for _, row in matched_df.head(top_n).iterrows():
            print(f"Recipe: {row['recipe_name']} | Match Score: {row['match_score']:.2f}%")
            print(f"Ingredients: {row['ingredients']}\n")

    # Convert to a list of dictionaries
    results = [{"name": row['recipe_name'], "score": row['match_score']} for _, row in matched_df.head(top_n).iterrows()]

    return results


# Function for greedy algorithm
def greedy_recommender(df, user_ingredients, top_n=5):
    user_ingredients = [i.lower().strip() for i in user_ingredients]

    def greedy_score(recipe_ingredients):
        matched = set(recipe_ingredients).intersection(user_ingredients)
        return (len(matched) / len(recipe_ingredients)) * 100

    df['match_score'] = df['ingredients_list'].apply(greedy_score)

    top_matches = df[df['match_score'] > 0].sort_values(by='match_score', ascending=False).head(top_n)

    # Convert to a list of dictionaries
    results = [{"name": row['recipe_name'], "score": row['match_score']} for _, row in top_matches.iterrows()]

    return results
from dataPreprocess import clean_recipe_data
from recommendersAlgorithm import string_match_recommender, brute_force_recommender, greedy_recommender
df = clean_recipe_data("dataset/recipes.csv")