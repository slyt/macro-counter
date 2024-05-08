from recipe_parser import RecipeParser

parser = RecipeParser(
    api_key="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", # this can be anything if using llama-cpp-python server
    base_url="http://localhost:8080/v1", # url of the llama-cpp-python server, execute start_server.sh
    model="function-calling" # see server_config.json for model alias
)

recipe_url = "https://joyfoodsunshine.com/the-most-amazing-chocolate-chip-cookies/"
recipe_text = parser.fetch_recipe(recipe_url)
recipe = parser.create_completion(recipe_text)
recipe = parser.convert_quantities(recipe) # convert to pint quantities

print(f"# {recipe.name}")
print("## Ingredients")
for ingredient in recipe.ingredients:
    print(f"- {ingredient.name}: {ingredient.quantity}")
print("## Directions")
for idx, direction in enumerate(recipe.directions):
    print(f"{idx+1}. {direction}")
