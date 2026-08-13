# BMI - Body Mass Index
# https://en.wikipedia.org/wiki/Body_mass_index

'''
BMI = mass(kg) / height(m)**2  (The BMI is expressed in kg/m2)

BMI,            basic categories
Category	                        BMI (kg/m2)[c]	
Underweight (Severe thinness)	    < 16.0	
Underweight (Moderate thinness)	    16.0–16.9	
Underweight (Mild thinness)	        17.0–18.4	
Normal range	                    18.5–24.9	
Overweight (Pre-obese)	            25.0–29.9	
Obese (Class I)	                    30.0–34.9	
Obese (Class II)	                35.0–39.9	
Obese (Class III)	                ≥ 40.0	

'''
mass = float(input("Type your mass (kg)\n"))
height = float(input("Type your height (m.сm)\n"))
# Here we can validate the input values how much height usually can be people.
# If typed more than 3 meters - say "Wow! You are very tall, but people usually below 3 meters."
# Same with mass - we can limit the normal range and handle exceptions

bmi = mass / (height**2)

print(f"Your BMI: {bmi:.1f}")
if bmi < 16.0:
    diagnosis = "Underweight (Severe thinness)"
elif bmi >= 16.0 and bmi <= 16.9:
    diagnosis = "Underweight (Moderate thinness)"
elif bmi >= 17.0 and bmi <= 18.4:
    diagnosis = "Underweight (Mild thinness)"
elif bmi >= 18.5 and bmi <= 24.9:
    diagnosis = "Normal range"
elif bmi >= 25.0 and bmi <= 29.9:
    diagnosis = "Overweight (Pre-obese)"
elif bmi >= 30.0 and bmi <= 34.9:
    diagnosis = "Obese (Class I)"
elif bmi >= 35.0 and bmi <= 39.9:
    diagnosis = "Obese (Class II)"
elif bmi >= 40.0:
    diagnosis = "Obese (Class III)"
else:
    diagnosis = "We don't know. Сonsult a doctor"
    
print(f"Diagnosis: {diagnosis}")

start_calculate_normal_mass = input("Do you want to calculate your normal mass? Type yes/no\n")

if start_calculate_normal_mass.lower() == "yes":
    if bmi >= 18.5 and bmi <= 24.9:
        print("You already have normal mass")
    else:
        normal_bmi_range_start = 18.5
        normal_bmi_range_end = 24.9
        normal_mass_range_start = normal_bmi_range_start * (height**2)
        normal_mass_range_end = normal_bmi_range_end * (height**2)
        normal_mass_average = (normal_mass_range_start + normal_mass_range_end) / 2
        normal_mass_dispersion = (normal_mass_range_end - normal_mass_range_start) / 2
        print(f"Your normal mass should have {normal_mass_average:.2f} +- {normal_mass_dispersion:.2f} kg")
if start_calculate_normal_mass == "no":
    print("Ok, good luck!")