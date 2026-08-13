'''
https://py-pkgs.org/welcome


[tool.poetry] — метаданные проекта
Параметр	Пример	Описание
name	"my_project"	Название проекта
version	"0.1.0"	Версия в формате MAJOR.MINOR.PATCH
description	"Описание проекта"	Краткое описание
authors	["Alice <alice@example.com>"]	Список авторов
license	"MIT"	Лицензия проекта
readme	"README.md"	Путь к файлу README
homepage	"https://example.com"	Домашняя страница проекта
repository	"https://github.com/user/repo"	Репозиторий проекта
documentation	"https://docs.example.com"	Документация

[tool.poetry.dependencies] — зависимости проекта
Пример	Описание
python = "^3.11"	Версия Python
requests = "^2.31"	Зависимость с ограничением версии
numpy = ">=1.25,<2.0"	Диапазон версий
pandas = { version = "^2.0", optional = true }	Опциональная зависимость

[tool.poetry.dev-dependencies] — зависимости для разработки
Пример	Описание
pytest = "^7.0"	Тестирование
black = "^24.3"	Форматирование кода
mypy = "^1.5"	Статическая типизация

[build-system] — сборка проекта (PEP 518)
Параметр	Пример	Описание
requires	["poetry-core>=1.4.0"]	Пакеты для сборки проекта
build-backend	"poetry.core.masonry.api"	Модуль, выполняющий сборку

[tool.<tool_name>] — конфигурация инструментов
Пример	Описание
[tool.black]	line-length = 88
target-version = ["py311"]
[tool.isort]	profile = "black"
'''

[build-system]
requires = ["setuptools>=42"]           # зависимости для сборки (минимальная версия setuptools 42)
build-backend = "setuptools.build_meta" # какой бэкенд будет собирать проект

[project]
name = "console_controls"                # имя пакета (pip install mypack01)
version = "0.1.0"                        # версия (SemVer: major.minor.patch)
description = "Console controls package" # описание
requires-python = ">=3.10"               # минимальная версия Python
