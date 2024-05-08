import openai
import instructor
import requests
from bs4 import BeautifulSoup

from pint import UnitRegistry
ureg = UnitRegistry()
import models

MODEL = "function-calling"  # see server_config.json for model alias

client = openai.OpenAI(
    api_key = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", # can be anything
    base_url = "http://localhost:8080/v1" # NOTE: Replace with IP address and port of your llama-cpp-python server
)

# Enables `response_model`
client = instructor.patch(client=client)

def fetch_recipe(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    # Send a request to the URL with custom headers
    response = requests.get(url, headers=headers)
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the content of the page with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract elements as needed, here assuming the recipe is in a <div> with class "recipe"
        recipe_content = soup.find('div', class_="wprm-recipe-container")
        if recipe_content:
            return recipe_content.get_text(strip=True)
        else:
            return "Recipe not found."
    else:
        return "Failed to retrieve the webpage."

recipe_url = "https://joyfoodsunshine.com/the-most-amazing-chocolate-chip-cookies/"
recipe_text = fetch_recipe(recipe_url) # get recipe text from URL using beautifulsoup

recipe = client.chat.completions.create(
    model=MODEL,
    response_model=models.Recipe,
    messages=[
        {"role": "user", "content": f"Extract ingredients: {recipe_text}"},
    ]
)
print(recipe.ingredients)
print(recipe.directions)
print("############")
print(f"Parsed recipe {recipe.name} as Recipe pydantic model:")
# loop through directions and print step and index too
for idx, direction in enumerate(recipe.directions):
    print(f"Step {idx+1}: {direction}")

assert isinstance(recipe, models.Recipe)


recipe_pint = models.RecipePint.from_recipe(recipe)
assert isinstance(recipe_pint, models.RecipePint)
print("############")
print(f"Parsed recipe {recipe_pint.name} as RecipePint pydantic model:")
# View ingredients with their pint quantities
for ingredient in recipe_pint.ingredients:
    print(ingredient)

for idx, direction in enumerate(recipe_pint.directions):
    print(f"Step {idx+1}: {direction}")



