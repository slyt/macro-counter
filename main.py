from recipe_parser import RecipeParser
import fooddatacentral as fdc
from models import RecipePint
import pickle

# load API key from .env file
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("FOOD_DATA_CENTRAL_API_KEY")

parser = RecipeParser(
    api_key="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", # this can be anything if using llama-cpp-python server
    base_url="http://localhost:8080/v1", # url of the llama-cpp-python server, execute start_server.sh
    model="function-calling" # see server_config.json for model alias
)

recipe_url = "https://joyfoodsunshine.com/the-most-amazing-chocolate-chip-cookies/"
recipe = parser.recipe_from_url(recipe_url) # fetch recipe from URL and convert to RecipePint

# save recipe in recipes directory so we don't need to fetch it every time
recipe_name = recipe.name.replace(' ','_')
print(f"Saving recipe `{recipe_name}` to recipes/{recipe.raw_text_hash}.pkl")
with open(f"recipes/{recipe.raw_text_hash}.pkl", "wb") as output_file:
    pickle.dump(recipe, output_file)
recipe=None
recipe_hash = "a34b0caf0e411293c2b36b606fbf2627"
with open(f"recipes/{recipe_hash}.pkl", "rb") as input_file:
    recipe = pickle.load(input_file)

# Inspect the recipe to ensure it was loaded correctly
print(f"# {recipe.name}")
print("## Ingredients")
for ingredient in recipe.ingredients:
    print(f"- {ingredient.name}: {ingredient.quantity}")

# print("## Directions")
# for idx, direction in enumerate(recipe.directions):
#     print(f"{idx+1}. {direction}")


