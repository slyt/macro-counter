# macro-counter
Using LLMs to count macro nutrients (macros)


## Setup

Tested using Nvidia GPU for acceleration. If using Nvidia, ensure you have compatible CUDA runtime (run `nvidid-smi`) and CUDA toolkit (run `nvcc --version`) installed for building llama-cpp-python.

Copy `.env_example` to `.env` and put in your API key from [FoodData Central](https://fdc.nal.usda.gov/api-key-signup.html)

```sh
python -m venv env
source env/bin/activate
pip install -r requirements.txt
CMAKE_ARGS="-DLLAMA_CUDA=on" pip install llama-cpp-python --force-reinstall --no-cache-dir
python download_models.py
./start_server.sh &
python main.py
```

### TODO

- [x] Parse recipes from the web
- [x] Parse strings to pint quantities
- [x] Add ability to cache recipes
- [x] Calculate macro needs based on height, weight, age, gender
- [ ] Add RecipeBook object that keeps track of cached recipes
- [ ] Get macro values for each ingredient
- [ ] Adjust macros based on goals: lose weight, build muscle, maintain
- [ ] Create meal plan for individual based on recipes and macro requirements
- [ ] Create meal plan for groups of people
- [ ] Create shopping list based meal plan
- [ ] Calculate prices using grocery stores' APIs 

### Built using
- [llama-cpp-python](https://github.com/abetlen/llama-cpp-python/tree/main) for serving the LLM backends, function calling
- [pydantic](https://docs.pydantic.dev/latest/) for object orientation and typing
- [instructor](https://jxnl.github.io/instructor/) for generating instances of pydantic models using LLM's
- [pint](https://pint.readthedocs.io/en/stable/) for unit conversion
- [fooddatacentral](https://pypi.org/project/fooddatacentral/) client for USDA FoodData Central API
- [USDA FoodData Central API](https://fdc.nal.usda.gov/api-guide.html): `U.S. Department of Agriculture, Agricultural Research Service. FoodData Central, 2019. fdc.nal.usda.gov.`

### See Also

- [Macro Counting with Python](https://medium.com/@adamliscia/macro-counting-with-python-10182147278) by @AdamLiscia