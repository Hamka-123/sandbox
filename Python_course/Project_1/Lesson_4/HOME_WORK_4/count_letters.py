# input text -> We learn Python -> string
#               01234567890123456789 ->13 letters, 2 spaces
# print count letters (skip spaces) 

# V2
# print count uppercase letters and lowercase letters

text = str(input("Type the text:\n"))
text_without_spaces = text.replace(" ", "")
print(f'Count letters in text: {len(text_without_spaces)}')
print(f'Count whitespaces in text: {text.count(" ")}')

# V2
uppercase_count = 0
lowercase_count = 0

for letter in text_without_spaces:
    if letter.isupper():
        uppercase_count += 1
    elif letter.islower():
        lowercase_count += 1
print(f'Uppercase letters count: {uppercase_count}')
print(f'Lowercase letters count: {lowercase_count}')      
