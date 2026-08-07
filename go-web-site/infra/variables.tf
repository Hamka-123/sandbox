variable "location" {
  type        = string
  default     = "westeurope"
  description = "Регион Azure"
}

variable "resource_group_name" {
  type        = string
  default     = "rg-go-web-app-alina"
  description = "Имя группы ресурсов"
}

variable "container_group_name" {
  type        = string
  default     = "aci-go-web-app"
  description = "Имя Container Group"
}

variable "dns_name_label" {
  type        = string
  default     = "go-web-app-unique-dns" # Должно быть уникальным в пределах региона Azure
  description = "DNS префикс для публичного IP"
}

variable "container_name" {
  type        = string
  default     = "go-web-app"
  description = "Имя контейнера внутри группы"
}

variable "container_port" {
  type        = number
  default     = 8080
  description = "Порт, который слушает приложение"
}

variable "ghcr_username" {
  type        = string
  default     = "Hamka-123"
  description = "Имя пользователя GitHub"
}

variable "ghcr_token" {
  type        = string
  sensitive   = true
  description = "GitHub Personal Access Token (PAT) с правами read:packages"
}

variable "container_image" {
  type        = string
  default     = "ghcr.io/hamka-123/go-web-app"
  description = "Базовый путь к образу без тега"
}

variable "image_tag" {
  type        = string
  default     = "latest"
  description = "Тег образа (передается из CI/CD)"
}
