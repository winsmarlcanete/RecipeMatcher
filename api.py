from fastapi import FastAPI
from pydantic import BaseModel
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

class Ingredients(BaseModel):
    ingredients: list[str]
    algorithm: str

app = FastAPI()

@app.post("/recommend/")
def recommend(data: Ingredients):
    logging.debug(f"Received ingredients: {data.ingredients}")
    logging.debug(f"Received algorithm: {data.algorithm}")
    # Your recommendation logic goes here...
    return {"message": "Received data successfully", "ingredients": data.ingredients}