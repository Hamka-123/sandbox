variable "base_name"           { default = "Alina-module" }

variable "my_public_ip" {
    type        = string
    default     = "212.178.18.103"
    description = "Мой публичный IP для ограничения доступа по SSH"
}
variable "resource_group_name" {}
variable "location" {}
