# # from google import genai

# # # Initialize the client with your key
# # client = genai.Client(api_key="KEY")

# # # Make a request using the default modern model
# # response = client.models.generate_content(
# #     model="gemini-3.6-flash",
# #     contents="Explain how quantum computing works in one sentence.",
# # )

# # print(response.text)

# from google import genai

# # Инициализируем клиент с вашим ключом
# client = genai.Client(api_key="KEY")

# # Создаем сессию чата с использованием актуальной модели
# chat = client.chats.create(model="gemini-3.6-flash")

# # Отправляем сообщение в рамках чата
# response = chat.send_message("Какой сегодня день?")

# print(response.text)

from google import genai

client = genai.Client()
# # Получаем и выводим список всех доступных моделей
# for model in client.models.list():
#     print(model.name)

MODEL = "gemini-3.5-flash-lite"

prompt = """
Explain how AI works in a one sentence
"""

prompt1 = """
You are the AI teacher. Explain how AI works in a one sentence
"""
prompt2 = """
You are the AI teacher. Explain how AI works in a one sentence. Answer on Russian, not more then 10 words.
"""

# prompt3 = input("Enter your question: ")

while True:
    print("Hello from my first AI app!!!")
    
    decision = "y"
    if decision == "n":
        break
    
    prompt = input("Input your question: ")
    interaction = client.interactions.create(
        model=MODEL,
        input=prompt
    )
    print(interaction.output_text)
    decision = input("Ask another question? y/n: ")