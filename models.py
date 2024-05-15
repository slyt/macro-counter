from pydantic import BaseModel, field_serializer
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
    
    @field_serializer('quantity', when_used="json")
    def serialize_quantity(quantity: pint.Quantity): # converts quantity to string for JSON serialization
        return str(quantity)
    


class Recipe(BaseModel):
    name: str
    ingredients: List[Ingredient]
    directions: List[str]
    raw_text: str
    raw_text_hash: str


class RecipePint(BaseModel):
    name: str
    ingredients: List[IngredientPint] 
    directions: List[str]
    raw_text: str
    raw_text_hash: str

    # Conversion from Recipe to RecipePint
    @classmethod
    def from_recipe(cls, recipe: Recipe) -> 'RecipePint':
        ingredients_pint = [IngredientPint.from_ingredient(ing) for ing in recipe.ingredients]
        return cls(name=recipe.name, ingredients=ingredients_pint, directions=recipe.directions, raw_text=recipe.raw_text, raw_text_hash=recipe.raw_text_hash)

    def save_to_json(self, filename: str): # Use pickle instead to retain the pint.Quantity objects
        with open(filename, 'w') as f:
            f.write(self.model_dump_json())

    def print_ingredients(self) -> None:
        for ingredient in self.ingredients:
            print(ingredient)

    class Config:
        arbitrary_types_allowed = True

class Nutrient(BaseModel):
    nutrientId: int 
    nutrientName: str
    nutrientNumber: str
    unitName: str
    derivationCode: Optional[str] = None
    derivationDescription: Optional[str] = None
    derivationId: Optional[int] = None
    value: float
    foodNutrientSourceId: Optional[int] = None
    foodNutrientSourceCode: Optional[int] = None
    foodNutrientSourceDescription: Optional[str] = None
    rank: int
    indentLevel: int
    foodNutrientId: int
    percentDailyValue: Optional[int] = None  # Optional since not all nutrients have this field

class ProductDetails(BaseModel):
    fdcId: int # required
    description: str # required
    dataType: str # required
    gtinUpc: Optional[str] = None
    publishedDate: Optional[str] = None
    brandOwner: Optional[str] = None
    brandName: Optional[str] = None
    ingredients: Optional[str] = None
    marketCountry: Optional[str] = None
    foodCategory: str
    modifiedDate: Optional[str] = None
    dataSource: Optional[str] = None
    packageWeight: Optional[str] = None
    servingSizeUnit: Optional[str] = None
    servingSize: Optional[float] = None
    householdServingFullText: Optional[str] = None
    tradeChannels: Optional[List[str]] = None
    allHighlightFields: Optional[str] = None
    score: Optional[float] = None
    microbes: Optional[List] = None
    foodNutrients: List[Nutrient]
    finalFoodInputFoods: List
    foodMeasures: List
    foodAttributes: List
    foodAttributeTypes: List
    foodVersionIds: List
    shortDescription: Optional[str] = None
    commonNames: Optional[str] = None
    additionalDescriptions: Optional[str] = None
    foodCode: Optional[int] = None
    foodCategoryId: Optional[int] = None
    ndbNumber: Optional[str] = None
    mostRecentAcquisitionDate: Optional[str] = None
