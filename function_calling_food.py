import openai
import instructor

import models

MODEL = "function-calling"  # see server_config.json for model alias

client = openai.OpenAI(
    api_key = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", # can be anything
    base_url = "http://localhost:8080/v1" # NOTE: Replace with IP address and port of your llama-cpp-python server
)

# Enables `response_model`
client = instructor.patch(client=client)


recipe = client.chat.completions.create(
    model=MODEL,
    response_model=models.Recipe,
    messages=[
        {"role": "user", "content": "Extract ingredients: 2 slices sandwich bread 2 tablespoons peanut butter 2 teaspoons grape jelly or 2 teaspoons strawberry jam "},
    ]
)
print(recipe.ingredients)

assert isinstance(recipe, models.Recipe)


