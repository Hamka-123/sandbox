terraform {
  required_version = ">= 1.0"

  backend "azurerm" {
    resource_group_name  = "tfstate-rg"
    storage_account_name = "tfstatestorage2079"
    container_name       = "tfstate-container"
    key                  = "alina.tfstate"
  }
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.location
}

resource "azurerm_container_group" "aci" {
  name                = var.container_group_name
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  ip_address_type     = "Public"
  dns_name_label      = var.dns_name_label
  os_type             = "Linux"

  # Учетные данные для скачивания образа из GHCR
  image_registry_credential {
    server   = "ghcr.io"
    username = var.ghcr_username
    password = var.ghcr_token
  }

  # Описание контейнера
  container {
    name = var.container_name
    # ВАЖНО: передаем динамический digest (ghcr.io/hamka-123/go-web-app@sha256:...)
    # Формируем прямую ссылку: "ghcr.io/hamka-123/go-web-app:v1.0.4"
    image  = "${var.container_image}:${var.image_tag}"
    cpu    = "0.5"
    memory = "1.5"

    ports {
      port     = var.container_port
      protocol = "TCP"
    }

    environment_variables = {
      "PORT" = tostring(var.container_port)
    }
  }
}
