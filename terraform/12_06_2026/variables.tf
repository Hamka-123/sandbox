variable "resource_group_name" {
  description = "Имя ресурсной группы"
  type        = string
  default     = "student-rg-Alina"
}

variable "location" {
  description = "Регион для ресурсов"
  type        = string
  default     = "westeurope"
}

variable "base_name" {
  description = "Базовое имя для ВМ и связанных ресурсов"
  type        = string
  default     = "student-vm-Alina"
}

variable "admin_username" {
  description = "Имя администратора для ВМ"
  type        = string
  default     = "azureuser"
}

variable "admin_password" {
  description = "Пароль администратора для ВМ (используется в учебных целях)"
  type        = string
  sensitive   = true
  default     = "P@ssw0rd12345!"
}

variable "vm_count" {
  description = "Количество ВМ"
  type        = number
  default     = 3
}

variable "vm_size" {
  description = "Размер ВМ"
  type        = string
  default     = "Standard_B1s"
}

variable "vnet_cidr" {
  description = "Размер сети"
  type = string
  default = "10.0.0.0/16"
}
# variable "subnet_cidr" {
#   description = "Размер подсети"
#   type = list(string)
#   default = ["10.0.1.0/24"]
# }
