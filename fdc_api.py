import fooddatacentral as fdc
import json
import models

# load API key from .env file
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("FOOD_DATA_CENTRAL_API_KEY") # get the API key from the .env file

results_df = fdc.search(api_key,"crunchy peanut butter")

# print the first 5 rows of the results
print(results_df.head())

# pretty print the JSON of the first row
first_row_json = results_df.iloc[0].to_json()
pretty_json = json.loads(first_row_json)
#print(json.dumps(pretty_json, indent=4))


# parse into pydantic model for ProductDetails
product_details = models.ProductDetails(**pretty_json)
print(product_details)
nutrients = product_details.foodNutrients
for nutrient in nutrients:
    print(f"{nutrient.nutrientName}: {nutrient.value} {nutrient.unitName}")
        