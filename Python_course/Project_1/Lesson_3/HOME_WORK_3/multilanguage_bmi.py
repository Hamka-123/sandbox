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
lang_code = int(input('''
    0 - En 
    1 - He  
    2 - Ru        
                ''')
    )  
RLE = "\u202B"  # Right-To-Left Embedding
input_prompts = [
    [
    "Type your mass (kg)", 
    "הקלד את המסה שלך (ק״ג):",
    "Введите ваш вес (kg)",
    ],
    [
    "Type your height (m.сm)",
    "הקלד את הגובה שלך (מ׳.סמ׳):", 
    "Введите ваш рост (м.см)",
    ]
]

mass = float(input(input_prompts[0][lang_code]+'\n'))
height = float(input(input_prompts[1][lang_code]+'\n'))
# Here we can validate the input values how much height usually can be people.
# If typed more than 3 meters - say "Wow! You are very tall, but people usually below 3 meters."
# Same with mass - we can limit the normal range and handle exceptions

diagnosis_dict =[
    [
    "Underweight (Severe thinness)",
    "Underweight (Moderate thinness)",
    "Underweight (Mild thinness)",
    "Normal range",
    "Overweight (Pre-obese)",
    "Obese (Class I)",
    "Obese (Class II)",
    "Obese (Class III)",
    "We don't know. Сonsult a doctor"
     ],
    [
    "תת משקל (רזון חמור)",
    "תת משקל (רזון בינוני)",
    "תת משקל (רזון קל)",
    "טווח רגיל",
    "עודף משקל (טרום השמנת יתר)",
    "שמנים (מחלקה א')",
    "שמנים (Class II)",
    "שמנים (מחלקה III)",
    "אנחנו לא יודעים. פנה לרופא"
     ],
    [
    "Недостаточный вес (сильная худоба)",
    "Недостаточный вес (умеренная худоба)",
    "Недостаточный вес (легкая худоба)",
    "Нормальный диапазон",
    "Избыточный вес (предожирение)",
    "Ожирение (класс I)",
    "Ожирение (класс II)",
    "Ожирение (класс III)",
    "Мы не знаем. Проконсультируйтесь с врачом"
    ],
]
text_dict = [
    [
    "Your BMI: ",
    "ה-BMI שלך: ",
    "Ваш ИМТ: "
    ],
    [
    "Diagnosis: ",
    "אִבחוּן: ",
    "Диагноз: "
    ]
]

bmi = mass / (height**2)

if lang_code == 1:
    bmi_lang_string = f"{bmi:.1f}{text_dict[0][lang_code][::-1]}"
else:
    bmi_lang_string = f"{text_dict[0][lang_code]}{bmi:.1f}"

print(bmi_lang_string)

if bmi < 16.0:
    diagnosis = diagnosis_dict[lang_code][0]
elif bmi >= 16.0 and bmi <= 16.9:
    diagnosis = diagnosis_dict[lang_code][1]
elif bmi >= 17.0 and bmi <= 18.4:
    diagnosis = diagnosis_dict[lang_code][2]
elif bmi >= 18.5 and bmi <= 24.9:
    diagnosis = diagnosis_dict[lang_code][3]
elif bmi >= 25.0 and bmi <= 29.9:
    diagnosis = diagnosis_dict[lang_code][4]
elif bmi >= 30.0 and bmi <= 34.9:
    diagnosis = diagnosis_dict[lang_code][5]
elif bmi >= 35.0 and bmi <= 39.9:
    diagnosis = diagnosis_dict[lang_code][6]
elif bmi >= 40.0:
    diagnosis = diagnosis_dict[lang_code][7]
else:
    diagnosis = diagnosis_dict[lang_code][8]
    
if lang_code == 1:
    diagnosis_lang_string = f"{diagnosis} {text_dict[1][lang_code][::-1]}"
else:
    diagnosis_lang_string = f"{text_dict[1][lang_code]}{diagnosis}"
    
print(diagnosis_lang_string)