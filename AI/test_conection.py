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

interaction = client.interactions.create(
    model="gemini-3.8-flash",
    input="Explain how AI works in a few words"
)
print(interaction.output_text)