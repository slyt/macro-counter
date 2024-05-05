import fooddatacentral as fdc

# load API key from .env file
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("FOOD_DATA_CENTRAL_API_KEY")

results_df = fdc.search(api_key,"crunchy peanut butter")

# print the first 5 rows of the results
print(results_df.head())

# get the brandOwner of the first result
print(results_df.iloc[:].brandOwner)