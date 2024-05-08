from pydantic import BaseModel
from typing import List, Optional

import pint
ureg = pint.UnitRegistry()

class Ingredient(BaseModel):
    name: str
    quantity: float
    unit: str # TODO: 

# Parses quantities using pint so that we can do math on the quantities
# https://pint.readthedocs.io/en/stable/user/defining-quantities.html#using-string-parsing
class IngredientPint(BaseModel):
    name: str
    quantity: pint.Quantity

    class Config:
        arbitrary_types_allowed = True

    # Conversion from Ingredient to IngredientPint
    @classmethod
    def from_ingredient(cls, ingredient: Ingredient) -> 'IngredientPint':
        try:
            pint_quantity = ingredient.quantity * ureg(ingredient.unit) # e.g. 3.0 * ureg.tablespoon
        except pint.errors.UndefinedUnitError: # if unit is not defined, like 2 "eggs", convert it to dimensionless
            pint_quantity = ingredient.quantity * ureg.dimensionless
        return cls(name=ingredient.name, quantity=pint_quantity)


class Recipe(BaseModel):
    name: str
    ingredients: List[Ingredient]
    directions: List[str]

    
class RecipePint(BaseModel):
    name: str
    ingredients: List[IngredientPint] 
    directions: List[str]

    # Conversion from Recipe to RecipePint
    @classmethod
    def from_recipe(cls, recipe: Recipe) -> 'RecipePint':
        ingredients_pint = [IngredientPint.from_ingredient(ing) for ing in recipe.ingredients]
        return cls(name=recipe.name, ingredients=ingredients_pint, directions=recipe.directions)
    
    class Config:
        arbitrary_types_allowed = True