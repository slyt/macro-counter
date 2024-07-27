import pint
from typing import Dict, Union

class Person:
    
    ureg = pint.UnitRegistry()
    activity_multiplier_dict = {"sedentary": 1.2, "lightly_active": 1.375, "moderately_active": 1.55, "very_active": 1.725, "super_active": 1.9}

    def __init__(self, gender: str, age: int, weight: float, height: float, activity: str):
        if gender not in ["male", "female"]: # TODO: Calculate BMR for non-binary
            raise ValueError("gender must be either 'male' or 'female'")
        if activity not in self.activity_multiplier_dict:
            raise ValueError(f"activity must be one of {list(self.activity_multiplier_dict.keys())}")
        if age <= 0:
            raise ValueError("age must be a positive integer")
        if weight <=0:
            raise ValueError("weight must be a positive number")
        if height <=0:
            raise ValueError("height must be a positive number")
        
        self.gender = gender
        self.age = age
        self.weight = weight * self.ureg.pounds
        self.height = height * self.ureg.ft
        self.activity = activity
        self.bmr = self.calculate_bmr()
        self.tdee = self.calculate_tdee()
        self.macronutrients = self.calculate_macronutrients()

    def print_info(self):
        height_feet = int(self.height.to(self.ureg.feet).magnitude)
        height_inches = self.height.to(self.ureg.inch).magnitude % 12
        print("#############################################")
        print(f"weight (imperial): {self.weight.to(self.ureg.lb)}")
        print(f"height (imperial): {height_feet}ft {height_inches}in")
        print(f"weight (metric): {self.weight.to(self.ureg.kg)}")
        print(f"height (metric): {self.height.to(self.ureg.cm)}")
        print(f"Basal Metabolic Rate (BMR): {self.bmr} calories/day")
        print(f"Total Daily Energy Expenditure (TDEE): {self.tdee} calories/day")
        print("Macronutrient requirements:")
        for nutrient, info in self.macronutrients.items():
            print(f"{nutrient.capitalize()}: {info['grams']} ({info['calories']})")
        print("#############################################")

    def calculate_bmr(self) -> float:
        bmr = 10 * self.weight.to(self.ureg.kg).magnitude + 6.25 * self.height.to(self.ureg.cm).magnitude - 5 * self.age + 5
        if self.gender == "female":
            bmr = bmr - 161 - 5
        return bmr

    def calculate_tdee(self) -> pint.Quantity:
        bmr = self.calculate_bmr()
        bmr_adjusted = (bmr * self.activity_multiplier_dict[self.activity]) * self.ureg.kcal
        return bmr_adjusted

    def calculate_macronutrients(self) -> Dict[str, Dict[str, Union[pint.Quantity, pint.Quantity]]]:
        tdee = self.calculate_tdee()
        protein_grams = (1.5 * self.weight.to(self.ureg.kg).magnitude) * self.ureg.gram # 1.2 to 2.0 g/kg
        protein_calories = (4 * protein_grams.magnitude) * self.ureg.kcal # 4 g protein per kcal
        fat_calories = (0.25 * tdee.magnitude) * self.ureg.kcal # 0.20 to 0.35 of total kcal
        fat_grams = (fat_calories.magnitude / 9) * self.ureg.gram  # 9 kcal per gram of fat
        carbs_calories = (tdee - protein_calories - fat_calories) # remainder is carbs
        carbs_grams = (carbs_calories.magnitude / 4) * self.ureg.gram # 4 kcal per gram of carbs

        return {"protein": {"grams": protein_grams, "calories": protein_calories},
                "fat": {"grams": fat_grams, "calories": fat_calories},
                "carbs": {"grams": carbs_grams, "calories": carbs_calories}}

if __name__ == "__main__":
    # Usage
    height = 5 + 9/12 # 5ft 9in in feet
    person = Person(gender="male", age=25, weight=165, height=height, activity="moderately_active")
    person.print_info()
