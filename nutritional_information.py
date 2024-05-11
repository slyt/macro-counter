from models import Recipe, ProductDetails, Ingredient
import fooddatacentral as fdc
import os
from dotenv import load_dotenv
import json

# load API key from .env file
load_dotenv()
api_key = os.getenv("FOOD_DATA_CENTRAL_API_KEY")

def calculate_nutritional_information(recipe: Recipe) -> dict:
    total_nutrition = {} # dictionary to store the total nutritional information for the entire recipe

    for ingredient in recipe.ingredients:
        # Search for the ingredient in FoodData Central
        results_df = fdc.search(api_key, ingredient.name)

        # Assume the first result is the correct one
        first_row_json = results_df.iloc[0].to_json()
        product_details = ProductDetails(**json.loads(first_row_json))
        print("product_details.brandName:", product_details.brandName)
        print("product_details.description:", product_details.description)
        # dump and print product_details pydantic model as json product_details
        #print(product_details.model_dump_json())
        # pretty print json
        print(json.dumps(json.loads(product_details.model_dump_json()), indent=4))
        description = product_details.description
        brand_name = product_details.brandName
        serving_size_unit = product_details.servingSizeUnit
        serving_size = product_details.servingSize
        householdServingFullText = product_details.householdServingFullText

        # Scale the nutrient information by the amount of the ingredient in the recipe
        for nutrient in product_details.foodNutrients:
            if nutrient.nutrientName not in total_nutrition:
                print("Adding", nutrient.nutrientName)
                total_nutrition[nutrient.nutrientName] = 0
            print("nutrient.value", nutrient.value)
            print("###")
            if nutrient.derivationDescription is None:
                print("Warning!!! nutrient.derivationDescription is None, nutrient scaling may be incorrect")
            total_nutrition[nutrient.nutrientName] += nutrient.value * ingredient.quantity
        print("##################")
    return total_nutrition

if __name__ == "__main__":
    from recipe_parser import RecipeParser
    recipe_parser = RecipeParser(api_key = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", # can be anything
                                base_url = "http://localhost:8080/v1")
    recipe = recipe_parser.recipe_from_text("Extract ingredients: 2 slices sandwich bread 2 tablespoons peanut butter 2 teaspoons grape jelly or 2 teaspoons strawberry jam")

    total_nutrition = calculate_nutritional_information(recipe)
    print(total_nutrition)