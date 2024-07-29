import os
import json
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
from tools_nutrition import BrmCalculator, TDEECalculator, MacronutrientCalculator
from langchain_ollama.llms import OllamaLLM
from langchain_openai import OpenAI
from models import Recipe, Ingredient
load_dotenv()

import os
os.environ['OPENAI_MODEL_NAME'] = 'gpt-4o-mini'

llm = OpenAI()

# llm = OllamaLLM(
#     model = "llama3.1",
#     base_url = "http://localhost:11434")



# Instantiate tools
brm_calculator = BrmCalculator()
tdee_calculator = TDEECalculator()
macronutrient_calculator = MacronutrientCalculator()

# Define your agents with roles and goals
recipe_writer = Agent(
  role='Recipe Writer',
  goal='Write recipes that adhere to the dietary requirements and preferences of the target audience',
  backstory="""You work as a freelance recipe writer for a popular food blog. Your recipes are loved by readers for their simplicity and deliciousness. 
  You have a keen eye for detail and a passion for creating mouth-watering dishes.
  You love describing the food science behind each recipe and giving tips for perfecting the dish.
  """,
  verbose=True,
  allow_delegation=False,
  output_pydantic=Recipe,
  # You can pass an optional llm attribute specifying what model you wanna use.
  llm=llm
)

nutritionist = Agent(
  role='Nutritionist',
  goal='Give advice on the nutrition that a person requires based on their activity level, age, weight, gender, height',
  backstory="""You are an exceptional nutritionist with years of experience in helping people achieve their health goals through balanced diets.
  You have a deep understanding of nutritional science and a passion for promoting healthy eating habits.
  You believe that food is medicine and that a well-balanced diet is essential for overall well-being.
  You consult with the Client and gather information about their gender, age, weight, height, and activity level to calculate BMR and TDEE in order to give them information about their macronutrient requirements.
  """,
  verbose=True,
  llm= llm,
  allow_delegation=True,
  tools=[brm_calculator, tdee_calculator, macronutrient_calculator]
)

grocery_shopper = Agent(
    role='Grocery Shopper',
    goal='Build a grocery list based on the recipes provided by the Recipe Writer and the nutritional requirements given by the Nutritionist',
    backstory="""You are a meticulous grocery shopper who loves to find the best deals on fresh produce and quality ingredients.
    You optimize your shopping list by grouping items by category and store layout to save time and money.
    You have a keen eye for detail and always ensure that the ingredients you buy are of the highest quality.
    """,
    verbose=True,
    allow_delegation=True,
    llm=llm
)

client = Agent(
    role='Client',
    goal='Eat healthy and delicious meals that are tailored to your dietary requirements and preferences',
    backstory="""You are an average Joe who wants to eat healthier and improve your overall well-being.
    You are starting to pay more attention to your diet and are looking for easy and delicious recipes that fit your lifestyle.
    You prefer vegetarian meals, but will eat fish and chicken occasionally. Minimize gluten and dairy. Tortillas, yogurt, and cheese are okay.
    You have begun exercising regularly and want to make sure you are getting the right nutrition to support your fitness goals to build muscle and maintain a healthy weight.
    you have a busy schedule and find it challenging to plan and prepare nutritious meals.
    You are looking for a solution that provides you with easy-to-follow recipes and a convenient grocery list.
    Your physical attributes are as follows: gender: male, height: 162 cm, weight: 66 kg, age:31, activity level: moderately_active
    """,
    verbose=True,
    llm=llm
)



# Create tasks for your agents

consult_nutritionist = Task(
  description="""Consult with the Nutritionist to get your daily macronutrient requirements based on your activity level, age, weight, gender, and height.""",
  expected_output="Full analysis report in bullet points",
  llm=llm,
  agent=client
)

create_breakfast_recipe = Task(
  description="""Create a breakfast recipe for the Client that meets their macronutrient requirements (protein, fat, carbs, and overall Calories).""",
  expected_output="A breakfast Recipe that meets the dietary requirements of the Client",
  output_pydantic=Recipe,
  llm=llm,
  agent=recipe_writer,
  context = [consult_nutritionist] # prior context to reference
)

create_lunch_recipe = Task(
  description="""Create a lunch recipe for the Client that meets their macronutrient requirements (protein, fat, carbs, and overall Calories).""",
  expected_output="A lunch Recipe that meets the dietary requirements of the Client",
  output_pydantic=Recipe,
  llm=llm,
  agent=recipe_writer,
  context = [consult_nutritionist] # prior context to reference
)

create_dinner_recipe = Task(
  description="""Create a dinner recipe for the Client that meets their macronutrient requirements (protein, fat, carbs, and overall Calories).""",
  expected_output="A dinner Recipe that meets the dietary requirements of the Client",
  output_pydantic=Recipe,
  llm=llm,
  agent=recipe_writer,
  context = [consult_nutritionist] # prior context to reference
)

create_grocery_list = Task(
    description="""Consult with the Grocery Shopper to get a detailed grocery list based on the recipes you received from the Recipe Writer.""",
    expected_output="Grocery list with items categorized by type and annotated by which recipe they are assocated with",
    llm=llm,
    agent=client,
    context = [create_breakfast_recipe, create_dinner_recipe, create_lunch_recipe]
    )

tasks = [consult_nutritionist, 
         create_breakfast_recipe,
         create_lunch_recipe,
         create_dinner_recipe,
         create_grocery_list]

# Instantiate your crew with a sequential process
crew = Crew(
  agents=[recipe_writer, nutritionist, grocery_shopper, client],
  tasks=tasks,
  verbose=2, # You can set it to 1 or 2 to different logging levels
  llm=llm,
  max_rpm=3, # Maximum Rounds Per Message for the crew
  process = Process.sequential,
  memory=True # Uses embeddings to store the short-term memory of the crew
)

# Get your crew to work!
result = crew.kickoff()

# create timestamped directory to save task outputs for this crew run
import datetime
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
task_output_directory = f"task_output/task_outputs_{timestamp}"
os.makedirs(task_output_directory, exist_ok=True)

for i,task in enumerate(tasks):
    # Accessing the task output
    task_output = task.output

    print(f"Task Description: {task_output.description}")
    print(f"Task Summary: {task_output.summary}")
    print(f"Raw Output: {task_output.raw}")

    # save raw output to file
    with open(f"{task_output_directory}/task_{i}_output.txt", "w") as f:
        f.write(task_output.raw)

    if task_output.json_dict:
        print(f"JSON Output: {json.dumps(task_output.json_dict, indent=2)}")
        # save json output to file
        with open(f"{task_output_directory}/task_{i}_output.json", "w") as f:
            json.dump(task_output.json_dict, f, indent=2)
    if task_output.pydantic:
        print(f"Pydantic Output: {task_output.pydantic}")
        # save pydantic output as JSON to file
        with open(f"{task_output_directory}/task_{i}_output_pydantic.json", "w") as f:
            json.dump(task_output.pydantic.model_dump_json(), f, indent=2)

print("######################")
print(result)