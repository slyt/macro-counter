import pint
ureg = pint.UnitRegistry()

# TODO: Double check all the numbers to make sure they are correct according to the Mifflin-St Jeor Equation

gender = "male"
age = 25 # years
weight = 165 * ureg.pounds # kg
height = 5 * ureg.ft + 7 * ureg.inch # ft and inches
height_feet = int(height.to(ureg.feet).magnitude)  # Extract whole feet
height_inches = height.to(ureg.inch).magnitude % 12  # Extract remaining inches
activity = "moderately_active"

# Print the user's information
print("#############################################")
print(f"weight (imperial): {weight.to(ureg.lb)}")
print(f"height (imperial): {height_feet}ft {height_inches}in")
print(f"weight (metric): {weight.to(ureg.kg)}")
print(f"height (metric): {height.to(ureg.cm)}")
print("#############################################")

# Calculate the user's BMR using the Mifflin-St Jeor Equation
bmr = 10 * weight.to(ureg.kg).magnitude + 6.25 * height.to(ureg.cm).magnitude - 5 * age + 5
if gender == "female":
    bmr = bmr - 161

print(f"Basal Metabolic Rate (BMR): {bmr} calories/day")

# Calculate the user's Total Daily Energy Expenditure (TDEE) based on activity level
activity_multiplier_dict = {"sedentary": 1.2, "lightly_active": 1.375, "moderately_active": 1.55, "very_active": 1.725, "super_active": 1.9}
bmr_adjusted = (bmr * activity_multiplier_dict[activity]) * ureg.kcal
print(f"Total Daily Energy Expenditure (TDEE): {bmr_adjusted} calories/day")
print("#############################################")

# Calculate the user's macronutrient needs based on TDEE
protein_grams = (1.5 * weight.to(ureg.kg).magnitude) * ureg.gram # 1.2 to 2.0 g/kg
protein_calories = (4 * protein_grams.magnitude) * ureg.kcal # 4 g protein per kcal
fat_calories = (0.25 * bmr_adjusted.magnitude) * ureg.kcal # 0.20 to 0.35 of total kcal
fat_grams = (fat_calories.magnitude / 9) * ureg.gram  # 9 kcal per gram of fat
carbs_calories = (bmr_adjusted - protein_calories - fat_calories) # remainder is carbs
carbs_grams = (carbs_calories.magnitude / 4) * ureg.gram # 4 kcal per gram of carbs

print(f"Protein: {protein_grams} ({protein_calories})")
print(f"Fat: {fat_grams} ({fat_calories})")
print(f"Carbs: {carbs_grams} ({carbs_calories})")
print("#############################################")