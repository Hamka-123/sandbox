# pip install markdown-it-py
# from markdown_it import MarkdownIt
# import pathlib

# # Create parser
# md = MarkdownIt()

# # Get file data
# # with open(pathlib.Path(__file__).parent / "MD_structure.md" ) as f: 
# #   md_data = f.read()


# md_data = """
# #MD text
# asdasd

# ---
# """

# tokens = md.parse(md_data)

# for token in tokens: 
#     # print(token.tag)
#     print(token.type)
#     # print(token.content)
#     # print(token.as_dict)

# html = md.render(md_data)
# print(html)

import pathlib
from markdown_it import MarkdownIt

# Инициализируем парсер
md = MarkdownIt()

# Путь к вашему файлу в той же директории, где лежит скрипт
file_path = pathlib.Path(__file__).parent / "MD_structure.md"

# Читаем данные из файла
if file_path.exists():
    with open(file_path, "r", encoding="utf-8") as f:
        md_data = f.read()

    # Парсим текст в токены
    tokens = md.parse(md_data)
    html =  md.render(md_data)

    # Выводим детали по каждому токену
    for token in tokens:
        if token.content: 
            print(f"Type: {token.type} | Tag: {token.tag} | Content: {token.content}")
           
else:
    print(f"Файл {file_path.name} не найден!")
    
print(html)
        
