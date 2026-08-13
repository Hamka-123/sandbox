terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0" # Используем стабильную 3-ю версию, как на лекциях у Антона
    }
    tls = {
      source  = "hashicorp/tls"
      version = "~> 4.0"
    }
  }
}

provider "azurerm" {
  features {} # <-- Вот этот блок Azure требует в обязательном порядке!
}