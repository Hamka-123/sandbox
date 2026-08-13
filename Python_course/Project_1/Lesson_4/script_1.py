for i in "Hello 字 world":
    print(ord(i))
    
str1 = "הקלד את הגובה שלך (מ׳.סמ׳):"
print(str1)
str2 = str1[::-1]
print(str2)

str3 =  "ה-BMI שלך: "
print(str3)
str4 = str3[::-1]
print(str4)

input_prompts = [
    [
    "Type your mass (kg)", 
    "הקלד את המסה שלך (ק״ג):"[::-1],
    "Введите ваш вес (kg)",
    ],
    [
    "Type your height (m.сm)",
    ":("+"מ׳.סמ׳"[::-1]+") "+"הקלד את הגובה שלך"[::-1], #:(׳מס.׳מ) ךלש הבוגה תא דלקה
    "Введите ваш рост (м.см)",
    ]
]

print(input_prompts[0][1])
print(input_prompts[1][1])
    
