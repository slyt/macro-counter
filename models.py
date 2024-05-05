from pydantic import BaseModel
from typing import List

class Ingredient(BaseModel):
    name: str
    quantity: float
    unit: str

class Recipe(BaseModel):
    name: str
    ingredients: List[Ingredient]