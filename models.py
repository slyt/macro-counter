from pydantic import BaseModel
from typing import List, Optional

import pint
ureg = pint.UnitRegistry()

class Ingredient(BaseModel):
    name: str
    quantity: float
    unit: str

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

class Nutrient(BaseModel):
    nutrientId: int
    nutrientName: str
    nutrientNumber: str
    unitName: str
    derivationCode: str
    derivationDescription: str
    derivationId: int
    value: float
    foodNutrientSourceId: int
    foodNutrientSourceCode: str
    foodNutrientSourceDescription: str
    rank: int
    indentLevel: int
    foodNutrientId: int
    percentDailyValue: Optional[int] = None  # Optional since not all nutrients have this field

class ProductDetails(BaseModel):
    fdcId: int
    description: str
    dataType: str
    gtinUpc: str
    publishedDate: str
    brandOwner: str
    brandName: str
    ingredients: str
    marketCountry: str
    foodCategory: str
    modifiedDate: str
    dataSource: str
    packageWeight: str
    servingSizeUnit: str
    servingSize: float
    householdServingFullText: str
    tradeChannels: List[str]
    allHighlightFields: str
    score: float
    microbes: List
    foodNutrients: List[Nutrient]
    finalFoodInputFoods: List
    foodMeasures: List
    foodAttributes: List
    foodAttributeTypes: List
    foodVersionIds: List
    shortDescription: Optional[str] = None
    commonNames: Optional[str] = None
    additionalDescriptions: Optional[str] = None
    foodCode: Optional[str] = None
    foodCategoryId: Optional[str] = None
    ndbNumber: Optional[str] = None
    mostRecentAcquisitionDate: Optional[str] = None
