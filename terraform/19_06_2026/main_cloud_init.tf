resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.location
}

resource "azurerm_virtual_network" "vnet" {
  name                = "${var.base_name}-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
}

resource "azurerm_subnet" "subnet" {
  name                 = "${var.base_name}-subnet"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.1.0/24"]
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
    source_address_prefix      = var.my_public_ip # Твой IP
    destination_address_prefix = "*"
  }

  security_rule {
    name                       = "HTTP"
    priority                   = 1002
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "80"
    source_address_prefix      = "*" # HTTP доступен всем для проверки в браузере
    destination_address_prefix = "*"
  }
}

resource "azurerm_public_ip" "pip" {
  name                = "${var.base_name}-pip"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  allocation_method   = "Static"
  sku                 = "Standard"
}

resource "azurerm_network_interface" "nic" {
  name                = "${var.base_name}-nic"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.subnet.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.pip.id
  }
}

resource "azurerm_network_interface_security_group_association" "nic_assoc" {
  network_interface_id      = azurerm_network_interface.nic.id
  network_security_group_id = azurerm_network_security_group.nsg.id
}

# Генерация временного SSH-ключа, чтобы не мучиться с паролями
resource "tls_private_key" "ssh_key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

# resource "azurerm_linux_virtual_machine" "vm" {
#   name                = "${var.base_name}-vm"
#   resource_group_name = azurerm_resource_group.rg.name
#   location            = azurerm_resource_group.rg.location
#   size                = var.vm_size
#   admin_username      = var.admin_username

#   network_interface_ids = [azurerm_network_interface.nic.id]

#   admin_ssh_key {
#     username   = var.admin_username
#     public_key = tls_private_key.ssh_key.public_key_openssh
#   }

#   os_disk {
#     caching              = "ReadWrite"
#     storage_account_type = "Standard_LRS"
#   }

#   source_image_reference {
#     publisher = "Canonical"
#     offer     = "0001-com-ubuntu-server-focal"
#     sku       = "20_04-lts-gen2"
#     version   = "latest"
#   }

#   # СПОСОБ 1: Передача cloud-config
#   custom_data = base64encode(<<-EOF
#     #cloud-config
#     package_update: true
#     packages:
#       - nginx
#     write_files:
#       - path: /var/www/html/index.html
#         permissions: "0644"
#         content: |
#           <!doctype html>
#           <html lang="ru">
#             <head>
#               <meta charset="utf-8">
#               <title>Terraform cloud-init</title>
#             </head>
#             <body>
#               <h1>Nginx установлен через cloud-init</h1>
#               <p>Источник настройки: custom_data в azurerm_linux_virtual_machine.</p>
#             </body>
#           </html>
#     runcmd:
#       - systemctl enable nginx
#       - systemctl restart nginx
#   EOF
#   )
# }
resource "azurerm_linux_virtual_machine" "vm" {
  name                = "${var.base_name}-vm"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  size                = var.vm_size
  admin_username      = var.admin_username
  network_interface_ids = [azurerm_network_interface.nic.id]

  admin_ssh_key {
    username   = var.admin_username
    public_key = tls_private_key.ssh_key.public_key_openssh
  }

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-focal"
    sku       = "20_04-lts-gen2"
    version   = "latest"
  }

  # Оставляем чистый дефолтный Nginx, чтобы провиженеры могли его заменить
  custom_data = base64encode(<<-EOF
    #!/bin/bash
    apt-get update && apt-get install -y nginx
  EOF
  )

  # БЛОК CONNECTION — необходим для работы file и remote-exec
  connection {
    type        = "ssh"
    user        = var.admin_username
    private_key = tls_private_key.ssh_key.private_key_pem
    host        = azurerm_public_ip.pip.ip_address
  }

  # СПОСОБ 2: Передача файла по SSH во временную папку VM
  provisioner "file" {
    source      = "index.html"
    destination = "/tmp/index.html"
  }

  # СПОСОБ 2.5: remote-exec переносит файл и перезапускает веб-сервер
  provisioner "remote-exec" {
    inline = [
      "cloud-init status --wait", # Ждем, пока облако достроит машину
      "sudo mv /tmp/index.html /var/www/html/index.html",
      "sudo systemctl restart nginx"
    ]
  }

  # ДОБАВЛЯЕМ local-exec: Пишет отчет на твой MacBook
  provisioner "local-exec" {
    command = <<-EOT
      echo "VM Name: ${self.name}" > created-vm-info.txt
      echo "Public IP: ${azurerm_public_ip.pip.ip_address}" >> created-vm-info.txt
      echo "Nginx URL: http://${azurerm_public_ip.pip.ip_address}" >> created-vm-info.txt
      echo "Launch Date: $(date)" >> created-vm-info.txt
      echo "Created by local-exec." >> created-vm-info.txt
    EOT
  }
}

output "public_ip" {
  value = azurerm_public_ip.pip.ip_address
}
