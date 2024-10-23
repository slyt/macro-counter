from pydantic import BaseModel, Field, validate_arguments, ValidationError
from typing import ClassVar, Dict, List, Union
from crewai_tools import BaseTool


class BrmCalculator(BaseTool):
    name: str = "Basal Metabolic Rate (BMR) Calculator"
    # Clear description for what this tool is useful for, your agent will need this information to use it.
    description: str = "This tool calculates the Basal Metabolic Rate (BMR) for a person based on their gender (male or female), age, weight (in kg), height (in cm)"
    
    gender_list: ClassVar[List[str]] = ["male", "female"] # TODO: Need more research about nutrition for non-binary people

    @validate_arguments
    def _run(self, gender: str, age: int, weight: Union[float, int], height: float) -> str:
        if gender not in self.gender_list:
            raise ValueError(f"Invalid gender: {gender}, must be one of {self.gender_list}")
        return self.calculate_bmr(gender, age, weight, height)

    def calculate_bmr(self, gender: str, age: int, weight: float, height: float) -> float:
        bmr = 10 * weight + 6.25 * height - 5 * age + 5 # Mifflin-St Jeor Equation for BMR, weight in kg, height in cm
        if gender == "female":
            bmr = bmr - 161 - 5
        return str(bmr)


class TDEECalculator(BaseTool):
    name: str = "Total Daily Energy Expenditure (TDEE) Calculator"
    description: str = "This tool calculates the Total Daily Energy Expenditure (TDEE), in kcal, of a person based on their BMR and activity level: sedentary, lightly_active, moderately_active, very_active, super_active"

    activity_multiplier_dict: ClassVar[Dict[str, float]] = {"sedentary": 1.2, "lightly_active": 1.375, "moderately_active": 1.55, "very_active": 1.725, "super_active": 1.9}
    activity_list: ClassVar[List[str]] = ["sedentary", "lightly_active", "moderately_active", "very_active", "super_active"]
   
    def _run(self, bmr: float, activity_level: str) -> str:
        if activity_level not in self.activity_list:
            raise ValueError(f"Invalid activity level: {activity_level}. Must be one of {self.activity_list}")
        return str(self.calculate_tdee(bmr, activity_level))

    def calculate_tdee(self, bmr, activity_level) -> int:
        bmr_adjusted = (bmr * self.activity_multiplier_dict[activity_level])
        return int(bmr_adjusted)


class MacronutrientCalculator(BaseTool):
    name: str = "Macronutrient Calculator"
    description: str = "This tool calculates the macronutrient requirements (protein, fat, and carbs), in grams and calories, of a person based on their Total Daily Energy Expenditure (TDEE)"

    def _run(self, tdee: int, weight: Union[float, int]) -> str:
        result_dict = self.calculate_macronutrients(tdee, weight)
        print(str(result_dict))
        return str(result_dict)

    def calculate_macronutrients(self, tdee, weight) -> Dict[str, Dict[str, Union[float, float]]]:
        protein_grams = (1.5 * weight)                             # 1.2 to 2.0 g/kg
        protein_calories = (4 * protein_grams)                     # 4 g protein per kcal
        fat_calories = (0.25 * tdee)                               # 0.20 to 0.35 of total kcal
        fat_grams = (fat_calories / 9)                             # 9 kcal per gram of fat
        carbs_calories = (tdee - protein_calories - fat_calories)  # remainder is carbs
        carbs_grams = (carbs_calories / 4)                         # 4 kcal per gram of carbs

        return {"protein": {"grams": protein_grams, "calories": protein_calories},
                "fat": {"grams": fat_grams, "calories": fat_calories},
                "carbs": {"grams": carbs_grams, "calories": carbs_calories}}
