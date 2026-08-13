resource "random_pet" "random" {
  length    = "1"
  separator = "-"
  # Блок слежения (оставь пустым или удали, если не нужен)
  # keepers = {
  #     # Generate a new pet name each time we switch to a new AMI id
  #     # ami_id = var.ami_id
  # }
}

locals {
  # Здесь имя будет с подчеркиванием: resource_group_alina_just_oriole
  rg_name = "resource_group_alina_${random_pet.random.id}"
  # В именах Storage Account нельзя использовать дефисы или другие символы
  # А здесь мы говорим: "Возьми ID и замени все '_' на пустоту"
  raw_name = "saalina${replace(random_pet.random.id, "_", "")}"
  # Обрезаем имя, чтобы оно было максимум 24 символа
  # 0 — начинаем с первого символа
  # 24 — берем максимум 24 знака
  sa_name      = substr(local.raw_name, 0, 24)
  storage_name = ""
}

resource "local_file" "test" {
  filename = "test.txt"
  content  = random_pet.random.id
}

resource "azurerm_resource_group" "alina_group" {
  name     = local.rg_name
  location = "West Europe"
}

resource "azurerm_storage_account" "alina_storage_account" {
  # ПРАВИЛЬНО: local. (без s)
  name = local.sa_name
  # Ссылка на имя ресурсной группы
  resource_group_name = local.rg_name

  # Ссылка на локацию из той же группы (чтобы не дублировать "West Europe")
  location                 = azurerm_resource_group.alina_group.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  tags = {
    owner = "Alina" #var.owner_name
  }
}

# Неявная зависимость: Создается сама, когда ты ссылаешься на ID другого ресурса.
# 1. Сначала создаем виртуальную сеть
resource "azurerm_virtual_network" "nimbus_vnet" {
  name                = "nimbus-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = "West Europe"
  resource_group_name = azurerm_resource_group.alina_group.name # Ссылка!
}
# Azure Subnet не может существовать сам по себе — он всегда должен быть внутри виртуальной сети (VNet) и иметь имя.
# 2. Теперь создаем подсеть ВНУТРИ этой сети

resource "azurerm_subnet" "nimbus_vnet" {
  name                = "internal-subnet"
  resource_group_name = azurerm_resource_group.alina_group.name

  # Ссылка на имя VNet — это создает неявную зависимость!
  virtual_network_name = azurerm_virtual_network.nimbus_vnet.name

  # Указываем диапазон внутри 10.0.0.0/16
  address_prefixes = ["10.0.1.0/24"]
}
# Явная зависимость (depends_on): Используется, если связи в коде нет, но один ресурс должен ждать другой.
# resource "azurerm_virtual_machine" "vm" {
#     name                = "test"
#     location            = "West Europe"
#     vm_size             = "Standard_B1s"
#     resource_group_name = azurerm_resource_group.alina_group.name 
#     network_interface_ids = ["id"]
#     # ВАЖНО: Убираем "=", ставим пробел и скобки
#     storage_os_disk {
#         name              = "myosdisk1"
#         caching           = "ReadWrite"
#         create_option     = "FromImage"
#         managed_disk_type = "Standard_LRS"
#     }
#     depends_on = [azurerm_storage_account.alina_storage_account]
# }

# Визуализация: terraform graph | dot -Tpng > graph.png — превращает зависимости в схему.

# Таргетинг (-target): Позволяет обновить только один конкретный ресурс, игнорируя остальные.
# terraform apply -target=azurerm_public_ip.main
# Внимание: используй это только для фикса ошибок, в обычном режиме это нарушает целостность стейта.

# Параллелизм (-parallelism): По умолчанию 10 задач одновременно. Если Azure тормозит, можно уменьшить:
# terraform apply -parallelism=5
