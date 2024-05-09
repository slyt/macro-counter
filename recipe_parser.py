import openai
import instructor
import requests
from bs4 import BeautifulSoup
from pint import UnitRegistry
import models
import hashlib

class RecipeParser:
    def __init__(self, api_key, base_url, model="function-calling"):
        self.ureg = UnitRegistry()
        self.client = openai.OpenAI(api_key=api_key, base_url=base_url)
        self.client = instructor.patch(client=self.client)
        self.model = model

    @staticmethod
    def fetch_recipe(url) -> str:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            recipe_content = soup.find('div', class_="wprm-recipe-container")
            if recipe_content:
                return recipe_content.get_text(strip=True)
            else:
                return "Recipe not found."
        else:
            return "Failed to retrieve the webpage."

    def create_completion(self, recipe_text) -> models.Recipe:
        return self.client.chat.completions.create(
            model = self.model,
            response_model=models.Recipe,
            messages=[
                {"role": "user", "content": f"Extract ingredients: {recipe_text}"},
            ]
        )
    
    def convert_quantities(self, recipe) -> models.RecipePint:
        recipe_pint = models.RecipePint.from_recipe(recipe)
        return recipe_pint
    
    def recipe_from_url(self, url) -> models.RecipePint:
        recipe_text = self.fetch_recipe(url) # get recipe text from URL
        recipe = self.recipe_from_text(recipe_text)
        return recipe
    
    def recipe_from_text(self, recipe_text) -> models.RecipePint:
        recipe = self.create_completion(recipe_text) # convert string to Recipe object
        recipe.raw_text = recipe_text
        recipe.raw_text_hash = hashlib.md5(recipe_text.encode('utf-8')).hexdigest() # Used for unique filenames later
        recipe = self.convert_quantities(recipe) # convert to quantities from string to pint.Quantity
        return recipe