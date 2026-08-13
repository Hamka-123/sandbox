
'''
0 - 6 night
6 - 12 morning
12 - 18 afternoon
18 - 24 evening
'''
correct_langs = ["English", "Hebrew", "Russian"]
greetings = [
    ["Good night", "Good morning", "Good afternoon", "Good evening" ],
    ["לילה טוב", "בוקר טוב", "צהריים טובים", "ערב טוב" ],
    ["Спокойной ночи", "Доброе утро", "Добрый день", "Добрый вечер" ]
]
input_prompts = [
    "Enter time",
    "להזין זמן",
    "Введите время"
]


lang = input(f"Type the language: {correct_langs}\n") # Можно вывести меню языков с вводом индекса словаря и дальше язык не проверять 
"""
   lang_code = input('''
          0 - En 
          1 - He  
          2 - Ru        
                  ''')  
"""

time = int(input("Type the time:\n")) # и здесь потом вывести текст на нужном языке из input_prompts[lang_code]

if lang == correct_langs[0]:
    dictionary = greetings[0]
elif lang == correct_langs[1]:
    dictionary = greetings[1]
elif lang == correct_langs[2]:
    dictionary = greetings[2]
else:
    print ("Not correct language")
    exit()

if time >= 0 and time < 6: # 0 >= time < 6
    greeting = dictionary[0]
elif time >= 6 and time < 12: # 6 >= time < 12
    greeting = dictionary[1]
elif time >= 12 and time < 18: # 12 >= time < 18
    greeting = dictionary[2]
elif time >= 18 and time <= 24: # 18 >= time <= 24
    greeting = dictionary[3]
else:
    print ("Not correct time")
    exit()
    
print(greeting)
'''
ДЗ на v2:
перевернуть для иврита ::-1

unicode = ord("A")
char = chr("\u3333")
определить язык по одному символу

по языку ещё определить время

Или по языку выдать вопрос на нужном языке

BMI сделать мультиязычным

'''
