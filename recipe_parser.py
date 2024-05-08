import openai
import instructor
import requests
from bs4 import BeautifulSoup
from pint import UnitRegistry
import models

class RecipeParser:
    def __init__(self, api_key, base_url, model="function-calling"):
        self.ureg = UnitRegistry()
        self.client = openai.OpenAI(api_key=api_key, base_url=base_url)
        self.client = instructor.patch(client=self.client)
        self.model = model

    def fetch_recipe(self, url) -> str:
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