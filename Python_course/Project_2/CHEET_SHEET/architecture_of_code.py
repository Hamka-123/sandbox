"""
🎯 ШАПРАГАЛКА ПО АРХИТЕКТУРЕ КОДА

ПРИНЦИПЫ ЧИСТОГО КОДА:

SOLID:
S - Single Responsibility - один класс = одна ответственность
O - Open/Closed - открыт для расширения, закрыт для изменений  
L - Liskov Substitution - наследники должны заменять родителей
I - Interface Segregation - много специализированных интерфейсов
D - Dependency Inversion - зависимости от абстракций, а не реализаций

DRY - Don't Repeat Yourself - не повторяй код
KISS - Keep It Simple, Stupid - упрощай
YAGNI - You Ain't Gonna Need It - не делай на будущее
Law of Demeter - "Не разговаривай с незнакомцами"
*/

АРХИТЕКТУРНЫЕ ПОДХОДЫ:

TOP-DOWN (сверху вниз):
1. Думай как пользователь → 2. Проектируй API → 3. Реализуй
Лучше для: MVP, CRUD, известных требований

BOTTOM-UP (снизу вверх):
1. Анализируй домен → 2. Проектируй сущности → 3. Создавай API  
Лучше для: сложных систем, фреймворков, долгосрочных проектов

ПАТТЕРНЫ ПРОЕКТИРОВАНИЯ:

COMPOSITE (Компоновщик) - для древовидных структур:
Component → Leaf (File) + Composite (Folder)

FACADE (Фасад) - простой интерфейс для сложной системы:
FileSystemManager скрывает сложность FileSystemEntry

FACTORY (Фабрика) - создание объектов без new:
FileSystemManager.create_file() вместо FileEntry()

BUILDER (Строитель) - пошаговое создание сложных объектов:
ProjectBuilder().add_src().add_tests().build()

ПРАВИЛА КАЧЕСТВЕННОГО КОДА:

✅ Имена: понятные, в style языка, без сокращений
✅ Функции: 5-15 строк, одна ответственность
✅ Классы: открыты для расширения, закрыты для изменений
✅ Тесты: пиши тестируемый код с dependency injection
✅ Комментарии: объясняют "почему", а не "что"
*/

# ПРАКТИЧЕСКИЕ ПРИМЕРЫ:
"""
# ✅ ХОРОШО - Top-Down мышление
class FileSystemManager:
    def list_folder(self, path: str) -> List[FileItem]:
        """Удобный API для пользователя"""
        pass

# ✅ ХОРОШО - Bottom-Up мышление  
class FileSystemEntry(ABC):
    """Богатая доменная модель"""
    @abstractmethod
    def get_size(self) -> int: pass

# ✅ ХОРОШО - Composite Pattern
class FolderEntry(FileSystemEntry):
    def add(self, child: FileSystemEntry):  # Composite
        self._children.append(child)

# ✅ ХОРОШО - Dependency Injection
class FileSystemManager:
    def __init__(self, logger: Logger, factory: EntryFactory):
        self.logger = logger  # Зависимости извне
        self.factory = factory

# ❌ ПЛОХО - Нарушение SRP
class GodClass:
    def save_to_db(self): ...    # Работа с БД
    def send_email(self): ...    # Отправка почты
    def validate_data(self): ... # Валидация

# ❌ ПЛОХО - Нарушение DIP
class Service:
    def __init__(self):
        self.db = MySQLDatabase()  # Зависимость от конкретной реализации

# ❌ ПЛОХО - Нарушение DRY
def calculate_area1(self): return 3.14 * r * r  # Дублирование
def calculate_area2(self): return 3.14 * r * r  # Дублирование
'''
ЧЕК-ЛИСТ ПРИ РЕФАКТОРИНГЕ:

1. □ Класс делает только одну вещь? (SRP)
2. □ Можно ли расширить без изменений? (OCP)  
3. □ Зависимости от абстракций? (DIP)
4. □ Нет дублирования кода? (DRY)
5. □ Просто ли читать и понимать? (KISS)
6. □ Есть ли ненужная функциональность? (YAGNI)
7. □ Тесты покрывают ключевую логику?
8. □ Комментарии объясняют сложные решения?

ПОМНИ: Хорошая архитектура стоит дорого, но плохая - еще дороже!
'''