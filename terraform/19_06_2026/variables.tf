variable "resource_group_name" { default = "Alina-provisioners-rg" }
variable "location"            { default = "westeurope" }
variable "base_name"           { default = "Alina-provision" }
variable "vm_size"             { default = "Standard_B1s" }
variable "admin_username"      { default = "azureuser" }

variable "my_public_ip" {
    type        = string
    default     = "212.178.18.103" # ПОДСТАВЬ СЮДА СВОЙ IP (например, "178.20.30.40")
    description = "Мой публичный IP для ограничения доступа по SSH"
}