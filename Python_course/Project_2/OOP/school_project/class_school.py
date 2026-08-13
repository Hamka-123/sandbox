import pathlib
from typing import Dict, Set
from class_student.class_student import StudentV2
from class_group.class_group import Group

class School:
    school_name:str = 'Specter'
    address:str = 'city Tel-Aviv, street something'
    students:dict[str,StudentV2] #email:StudentV2
    courses:set[str]
    groups:dict[int , Group] #id:Group
    
    def __init__(self):
        self.students = {}
        self.courses = set()
        self.groups = {}
    
# === УПРАВЛЕНИЕ СТУДЕНТАМИ ===
    def import_students_from_csv(self,data_file:pathlib.Path) -> Dict[str, StudentV2]:
        """Импорт студентов из CSV файла в словарь"""
        try:
             with open(data_file) as f:
                self.students = {
                    student.email: student 
                    for student in (
                        StudentV2(*line.strip().split(","),None) 
                        for line in f.readlines()[1:]
                    )
                }
                print(f"✅ Загружено {len(self.students)} студентов")
                
        except FileNotFoundError:
            print(f"❌ Файл {data_file} не найден")
            return {}
        except Exception as e:
            print(f"❌ Ошибка при чтении файла: {e}")
            return {}
        
    
    def add_student(self, *new_student_data:tuple) -> None:
        """Добавляет студента в словарь
            _____________________________
        *new_student_data:
            first_name:str
            last_name:str
            email:str
            gender:str
            course:str
            balance:float
            group:str
        """
        new_student = StudentV2(*new_student_data, None)
                
        self.students[new_student.email] = new_student
        print(f"Студент {new_student} добавлен ")
    
    def update_student(self, email, **fields_to_update) -> None:
        """Обновляет данные студента

        Args:
            email:str - адрес почты студента какого хотим обновить
            ______________________________
            Доступные поля для обновления:
            first_name:str
            last_name:str
            email:str
            gender:str
            course:str
            balance:float
            group:str
            
        """
        self.students[email].change_fields(**fields_to_update)
        print(f"✅ Данные студента {email} обновлены: {fields_to_update}")
        
    def delete_student(self, email:str) -> bool:
        """Безопасное удаление с возвратом статуса"""
        if email in self.students:
            self.students.pop(email)
            print(f"✅ Студент {email} удалён")
            return True
        else:
            print(f"❌ Студент с email {email} не найден")
            return False        
        
    def get_all_students(self) -> Dict[str, StudentV2]:
        """Получение всех студентов"""
        return self.students
    
# === УПРАВЛЕНИЕ ГРУППАМИ ===
    def add_group(self, name:str, course:str) -> Group:
        group_obj = Group(name, course, [])
        self.groups[group_obj.id] = group_obj
        print(f"✅ Группа {name} добавлена")
        return group_obj
    
    def get_groups_info(self) -> None:
        """Получение информации о всех группах"""
        if not self.groups:
            print("❌ В школе нет групп")
            return
        
        print("\n📊 ИНФОРМАЦИЯ О ГРУППАХ:")
        for group_id, group_obj in self.groups.items():
            print(f"   Группа '{group_obj.name}' (ID: {group_id}):")
            print(f"      Курс: {group_obj.course}")
            print(f"      Студентов: {len(group_obj.attended_students)}/{group_obj.max_students}")
            print(f"      Студенты: {[s.email for s in group_obj.attended_students]}")
    
    
    def add_student_to_group(self, group_id: int, student_email: str) -> bool:
        """Добавить студента в группу"""
        group = self.groups.get(group_id)
        student = self.students.get(student_email)
        
        if not group or not student:
            print(f"❌ Группа или студент не найдены")
            return False
        group_obj = group.add_student(student)
        return group_obj
    
    def remove_student_from_group(self, group_id: int, student_email: str)-> bool:
        """Убрать студента из группы"""
        group = self.groups.get(group_id)
        student = self.students.get(student_email)
        
        if not group or not student:
            print(f"❌ Группа или студент не найдены")
            return False
        success = group.remove_student(student)
        return success
    
    def delete_group(self, group_id:int) -> bool:
        """Удалить группу"""
        if group_id in self.groups:
            self.groups.pop(group_id)
            print(f"✅ Группа {group_id} удалёна")
            return True
        else:
            print(f"❌ Группа с шв {group_id} не найдена")
            return False   
        
# === УПРАВЛЕНИЕ КУРСАМИ ===
    def fill_courses_from_students(self) -> Set:
        for student in self.students.values():
           self.courses.add(student.course.strip())
        print(f"✅ Загружено {len(self.courses)} курсов")
        return  self.courses   
    
    def get_courses_info(self):
        if not self.courses:
            print("❌ В школе нет курсов")
            return
        for course in self.courses:
            students_count = len([s for s in self.students.values() if s.course == course])
            return(f"Курс {course}: {students_count} студентов")
    
# === СИСТЕМНЫЕ МЕТОДЫ ===
    def get_school_info(self) -> Dict:
        """Получение общей информации о школе"""
        return {
            'school_name': self.school_name,
            'address': self.address,
            'total_students': len(self.students),
            'total_courses': len(self.courses),
            'total_groups': len(self.groups)
        }
    
