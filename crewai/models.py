from pydantic import BaseModel, field_serializer
from typing import List, Optional


class Ingredient(BaseModel):
    name: str
    quantity: float
    unit: str


class Recipe(BaseModel):
    name: str
    ingredients: List[Ingredient]
    directions: List[str]


class MealPlan(BaseModel):
    name: str
    recipes: List[Recipe]


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
