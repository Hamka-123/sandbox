from class_student.class_student import StudentV2


class Group:
    __id = 0
    name:str
    course:str
    attended_students:list[object]
    max_students = 20
    
    def __init__(self, name, course, attended_students):
        Group.__id += 1
        self.id = Group.__id 
        self.name = name
        self.course = course
        self.attended_students = attended_students if attended_students else []
    
    def can_add_student(self, student_obj: StudentV2) -> tuple[bool, str]:
        """Проверяет, можно ли добавить студента в группу"""
        if len(self.attended_students) >= self.max_students:
            return False, f"❌ Группа переполнена! Максимум: {self.max_students}"
        
        if student_obj in self.attended_students:
            return False, f"⚠️ Студент уже в группе"
            
        return True, "✅ Можно добавить"
    
    def validate_student_addition(self, student_obj: StudentV2) -> bool:
        """Валидация с выводом сообщений"""
        can_add, message = self.can_add_student(student_obj)
        if not can_add:
            print(message)
        return can_add
    
    def add_student(self, student_obj: StudentV2) -> bool:
        """Добавляет студента в группу после валидации"""
        if self.validate_student_addition(student_obj):
            self.attended_students.append(student_obj)
            student_obj.group = self.name
            print(f"✅ Студент {student_obj.email} добавлен в группу {self.name}")
            return True
            return True
        return False
    
    def remove_student(self, student_obj: StudentV2) -> bool:
        """Убирает студента из группы"""
        if student_obj in self.attended_students:
            self.attended_students.remove(student_obj)
            print(f"✅ Студент {student_obj.email} удален из группы {self.name}")
            return True
        print("❌ Студент не в группе!")
        return False
    
    def __repr__(self):
        return f"Group(id={self.id}, name='{self.name}', course='{self.course}', students={len(self.attended_students)})"