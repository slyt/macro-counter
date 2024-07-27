import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
from tools_nutrition import BrmCalculator, TDEECalculator, MacronutrientCalculator
from langchain_ollama.llms import OllamaLLM
from langchain_openai import OpenAI
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
  # You can pass an optional llm attribute specifying what model you wanna use.
  llm=llm
)

nutritionist = Agent(
  role='Nutritionist',
  goal='Give advice on the nutrition that a person requires based on their lifestyle, age, weight, gender, height, and health conditions',
  backstory="""You are an exceptional nutritionist with years of experience in helping people achieve their health goals through balanced diets.
  You have a deep understanding of nutritional science and a passion for promoting healthy eating habits.
  You believe that food is medicine and that a well-balanced diet is essential for overall well-being.
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
    You have begun exercising regularly and want to make sure you are getting the right nutrition to support your fitness goals to build muscle and maintain a healthy weight.
    you have a busy schedule and find it challenging to plan and prepare nutritious meals.
    You are looking for a solution that provides you with easy-to-follow recipes and a convenient grocery list.
    Your physical attributes are as follows: gender: male, height: 162 cm, weight: 66 kg, age:31, activity level: moderately_active
    """,
    verbose=True,
    llm=llm
)


# Create tasks for your agents

task1 = Task(
  description="""Consult with the Nutritionist to get a detailed analysis of your dietary requirements.""",
  expected_output="Full analysis report in bullet points",
  llm=llm,
  agent=client
)

task2 = Task(
  description="""Consult with the Recipe Writer to get list of breakfast, lunch, and dinner recipes that can be used for meal prepping for the week based on your dietary requirements and preferences.""",
  expected_output="List of recipes with ingredients with amount and directions of how to prep each meal",
  llm=llm,
  agent=client
)

task3 = Task(
    description="""Consult with the Grocery Shopper to get a detailed grocery list based on the recipes you received from the Recipe Writer.""",
    expected_output="Grocery list with items categorized by type",
    llm=llm,
    agent=client
    )

# Instantiate your crew with a sequential process
crew = Crew(
  agents=[recipe_writer, nutritionist, grocery_shopper, client],
  tasks=[task1, task2, task3],
  verbose=2, # You can set it to 1 or 2 to different logging levels
  llm=llm,
  process = Process.sequential
)

# Get your crew to work!
result = crew.kickoff()

print("######################")
print(result)