# https://registry.terraform.io/providers/hashicorp/azurerm/latest
# brew install azure-cli
# az account
# az account list


terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "4.69.0"
    }
    local = {
      source  = "hashicorp/local"
      version = "2.8.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "3.8.1"
    }
  }

  backend "azurerm" {
    use_cli              = true
    use_azuread_auth     = true
    storage_account_name = "tfstatestorage2079"
    container_name       = "tfstate-container"
    key                  = "alina.terraform.tfstate"

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
provider "local" {
  # Configuration options
}
provider "random" {
  # Configuration options
}