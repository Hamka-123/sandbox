# input phrase
# count, print words number
# words separators - list
WORDS_SEPARATORS = [" ", "\n", "!"]

test_phrase = "Привет! Как дела\n У меня всё хорошо!"

phrase = input("Введите фразу: ") or test_phrase

# Заменим все разделители на пробел
for sep in WORDS_SEPARATORS:
    phrase = phrase.replace(sep, " ")

# Теперь разбиваем по пробелам и фильтруем пустые строки
words = [word for word in phrase.split(" ") if word]

print(f"Количество слов: {len(words)}")

