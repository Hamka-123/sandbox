terraform {
    required_providers {
        azurerm = {
        source  = "hashicorp/azurerm"
        version = "4.69.0"
        }
    }
}
provider "azurerm" {
    # Configuration options
    features {
        virtual_machine {
        # Удалять системный диск вместе с виртуалкой
        delete_os_disk_on_deletion = true
        }
    }
}

# чтение из файла Terraform/DataSources/data.txt
data "local_file" "owner" {
    filename = "${path.module}/data.txt"
}
# !!!! нельзя использовать динамику в значениях !!!
# variable "rg_name" {
#     default = "${data.local_file.owner.content}_rs"
# }
locals {
    # Вот здесь вычислять динамические значения МОЖНО и нужно
    rg_name = "${chomp(data.local_file.owner.content)}_rg"
}
# сохранить сюда теги из azurerm_resource_group.name а потом использовать их при пересоздании этой ресурсной группы
data "azurerm_resource_group" "rg"{
    name = "Alina_from_data_3_rs"
}

output "owner" {
    value = data.local_file.owner
}
output "rg_backup_tags" {
    value = azurerm_resource_group.name.tags
}

# сделать ресурcную группу
resource "azurerm_resource_group" "name" {
    name = local.rg_name
    location = "West Europe"
    # tags = {
    #     env = "testing"
    # }
    # tags = data.azurerm_resource_group.rg.tags
    tags = output.rg_backup_tags
    lifecycle {
        create_before_destroy = true
        ignore_changes = [tags]
        #prevent_destroy = true
    }
}

#  использовать содержимое файла в имени ресурсной группы (пересоздание)
# изменить теги руками на портале
#  поставить все флаги лайфсайкл - проверить

# изменить содержимое файла
# попробовать удалить
# apply
# удалить на портале руками при наличии флага prevent_destroy


