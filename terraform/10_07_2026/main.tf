
# resource "azurerm_resource_group" "example" {
#   name     = "AL-resource-group"
#   location = "East US"
# }

data "azurerm_resource_group" "common" {
  name = "AL-resource-group"
}

variable "envs" {
  type = map(string)
  default = {
    "default" = "def",
    "dev"     = "devel",
    "prod"    = "production"
  }
}

resource "azurerm_storage_account" "default" {
  name                     = "al${var.envs[terraform.workspace]}"
  resource_group_name      = data.azurerm_resource_group.common.name
  location                 = data.azurerm_resource_group.common.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}
