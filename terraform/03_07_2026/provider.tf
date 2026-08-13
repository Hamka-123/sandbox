terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      # version = ">= 3.0" 
      version = "~> 3.116.0" # Это заблокирует переход на ломающую 4-ю версию
    }
    tls = {
      source  = "hashicorp/tls"
      version = "~> 4.0"
    }
  }
}

provider "azurerm" {
  features {}
}