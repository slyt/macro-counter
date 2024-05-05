# macro-counter
Using LLM to count macro nutrients


## Setup

Tested using Nvidia GPU for acceleration. If using Nvidia, ensure you have compatible CUDA runtime (run `nvidid-smi`) and CUDA toolkit (run `nvcc --version`) installed for building llama-cpp-python.

```sh
python -m venv env
source env/bin/activate
pip install -r requirements.txt
CMAKE_ARGS="-DLLAMA_CUDA=on" pip install llama-cpp-python --force-reinstall --no-cache-dir
python download_models.py
./start_server.sh &
python function_calling_food.py
```

### Built using

- [USDA FoodData Central API](https://fdc.nal.usda.gov/api-guide.html): `U.S. Department of Agriculture, Agricultural Research Service. FoodData Central, 2019. fdc.nal.usda.gov.`
- [llama-cpp-python](https://github.com/abetlen/llama-cpp-python/tree/main) for serving the LLM backends, function calling
- [pydantic](https://docs.pydantic.dev/latest/) for object orientation and typing
- [instructor](https://jxnl.github.io/instructor/) for generating instances of pydantic models using LLM's

### See Also

- [Macro Counting with Python](https://medium.com/@adamliscia/macro-counting-with-python-10182147278) by @AdamLiscia