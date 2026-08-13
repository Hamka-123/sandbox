variable "one" {
  default = "test"
}
variable "owner_name" {
  default     = "Alina"
  type        = string
  description = "My name for usage - объяснение в консоли для переменной если её запрашивает"
  /*
    string: любая последовательность символов в кавычках.
    number: целые числа или числа с плавающей точкой.
    bool: логические значения true или false.
    list: ["a", "b", "c"] — список элементов одного типа.
    map: { "key" = "value" } — набор пар.
    */
}
variable "instance_name" {
  type    = string
  default = "nimbus-server"
}

variable "port" {
  type    = number
  default = 0
}

variable "is_enabled" {
  type    = bool
  default = true
}

# Список строк (List of strings)
variable "users" {
  type    = list(string)
  default = ["Alina", "Dima"]
}

# Карта (Map of strings)
variable "tags" {
  type = map(string)
  default = {
    env     = "dev"
    project = "nimbus"
  }
}

# Использование в коде:
# var.users[0] -> "Alina"
# var.tags["env"] -> "dev"

# 3. Способы передачи значений и приоритет
# Когда у тебя нет default, значения нужно передать извне. Вот порядок от самого слабого к самому сильному (кто выше числом, тот и «папа»):

# Переменные окружения: export TF_VAR_port=80

# Файл terraform.tfvars: Автоматически подгружается.

# Файлы *.auto.tfvars: Подгружаются в алфавитном порядке.

# Аргументы командной строки: terraform apply -var="port=80" (самый высокий приоритет).

# Интерактивный режим: Если ты не использовал ни один из способов выше и нет default, Terraform сам остановится и выведет запрос Enter a value в консоли.