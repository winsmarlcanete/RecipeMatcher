from fastapi import FastAPI
from pydantic import BaseModel
import logging
from dataPreprocess import clean_recipe_data
from recommendersAlgorithm import string_match_recommender, brute_force_recommender, greedy_recommender

df = clean_recipe_data("dataset/recipes.csv")
# Set up logging
logging.basicConfig(level=logging.DEBUG)

class Ingredients(BaseModel):
    ingredients: list[str]
    algorithm: str

app = FastAPI()

@app.post("/recommend/")
def recommend(data: Ingredients):
    if data.algorithm == "String Match":
        results = string_match_recommender(df, data.ingredients)
    elif data.algorithm == "Brute Force":
        results = brute_force_recommender(df, data.ingredients)
    else:
        results = greedy_recommender(df, data.ingredients)

    return {"results": results}