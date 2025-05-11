#function for string match algorithm
def string_match_recommender(df, user_ingredients, top_n=5):
    user_ingredients = [i.lower().strip() for i in user_ingredients]

    df['match_score'] = df['ingredients_list'].apply(
        lambda ingredients: len(set(ingredients).intersection(user_ingredients))
    )

    return df[df['match_score'] > 0].sort_values(by='match_score', ascending=False).head(top_n)

#function for brute force algorithm
def brute_force_recommender(df, user_ingredients, top_n=5):
    user_ingredients = [i.lower().strip() for i in user_ingredients]

    def is_subset(ingredients, available):
        return all(item in available for item in ingredients)

    df['match_score'] = df['ingredients_list'].apply(
        lambda ingredients: len(ingredients) if is_subset(ingredients, user_ingredients) else 0
    )

    return df[df['match_score'] > 0].sort_values(by='match_score', ascending=False).head(top_n)

#function for greedy algorithm
def greedy_recommender(df, user_ingredients, top_n=5):
    user_ingredients = [i.lower().strip() for i in user_ingredients]

    def greedy_score(recipe_ingredients):
        matched = set(recipe_ingredients).intersection(user_ingredients)
        # Give higher score to recipes that use a large % of their ingredients
        return len(matched) / len(recipe_ingredients)

    df['match_score'] = df['ingredients_list'].apply(greedy_score)

    return df[df['match_score'] > 0].sort_values(by='match_score', ascending=False).head(top_n)
