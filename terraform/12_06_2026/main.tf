locals {
  # Мы берем CIDR всей сети из переменной и автоматически нарезаем ее на подсети!
  subnets = {
    frontend = cidrsubnet(var.vnet_cidr, 8, 1) # Получится 10.0.1.0/24
    backend  = cidrsubnet(var.vnet_cidr, 8, 2) # Получится 10.0.2.0/24
    dmz      = cidrsubnet(var.vnet_cidr, 8, 3) # Получится 10.0.3.0/24
  }
}

resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.location
}

resource "azurerm_virtual_network" "vnet" {
  name                = "${var.base_name}-vnet"
  address_space       = [var.vnet_cidr]
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
}

# resource "azurerm_subnet" "subnet" {
#   name                 = "${var.base_name}-subnet"
#   resource_group_name  = azurerm_resource_group.rg.name
#   virtual_network_name = azurerm_virtual_network.vnet.name
#   address_prefixes     = var.subnet_cidr
# }

resource "azurerm_subnet" "subnets" {
  for_each             = local.subnets
  name                 = "${var.base_name}-${each.key}-subnet" # Имя будет динамическим: ...-frontend-subnet и т.д.
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = [each.value] 
}

resource "azurerm_network_security_group" "nsg" {
  name                = "${var.base_name}-nsg"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  security_rule {
    name                       = "SSH"
    priority                   = 1001
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}

resource "azurerm_public_ip" "pip" {
  count               = var.vm_count
  name                = "${var.base_name}-pip-${count.index}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  allocation_method   = "Static"
  sku                 = "Standard"
}

# Сетевые карты (NIC) — убрали изнутри network_security_group_id
resource "azurerm_network_interface" "nic" {
  count               = var.vm_count
  name                = "${var.base_name}-nic-${count.index}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  ip_configuration {
    name                          = "internal"
    # subnet_id                     = azurerm_subnet.subnet.id
    subnet_id                     = azurerm_subnet.subnets["frontend"].id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.pip[count.index].id
  }
}

# ИСПРАВЛЕНИЕ: Отдельный ресурс для привязки NSG к каждой сетевой карте
resource "azurerm_network_interface_security_group_association" "nic_assoc" {
  count                     = var.vm_count
  network_interface_id      = azurerm_network_interface.nic[count.index].id
  network_security_group_id = azurerm_network_security_group.nsg.id
}

resource "azurerm_linux_virtual_machine" "vms" {
  count               = var.vm_count
  name                = "${var.base_name}-${count.index}"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  size                = var.vm_size

  network_interface_ids = [azurerm_network_interface.nic[count.index].id]

  admin_username = var.admin_username
  admin_password = var.admin_password
  disable_password_authentication = false

  os_disk {
    name              = "${var.base_name}-osdisk-${count.index}"
    caching           = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-focal" # Современный ID для Ubuntu 20.04
    sku       = "20_04-lts-gen2"
    version   = "latest"
  }

  tags = {
    environment = "student"
  }
}
