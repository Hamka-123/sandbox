resource "azurerm_resource_group" "rg" {
    name     = var.resource_group_name
    location = var.location
}

# module "network" {
#     source = "./network"
#     base_name = "Alina_submodule"
#     my_public_ip = "212.178.18.103"
#     resource_group_name = azurerm_resource_group.rg.name
#     location = azurerm_resource_group.rg.location
# }

# module "network" {
#     # Просто имя модуля из реестра
#     source  = "Azure/network/azurerm"
#     version = "5.3.0" # Для удаленных модулей ОЧЕНЬ рекомендуется фиксировать версию!

#     # Дальше твои параметры
#     resource_group_name = azurerm_resource_group.rg.name
#     address_spaces      = ["10.0.0.0/16"]
#     # ДОБАВЬ ЭТУ СТРОКУ (поставь true или false в зависимости от того, что требует логика модуля)
#     use_for_each = false   
# }
# module "private_network" {
#     # Используем Git по SSH-протоколу
#     source = "git@github.com:alina-devops/private-network-module.git?ref=v2.0.1"

#     base_name = "Alina_network_submodule_from_git"
# }
module "network" {
    # Фиксируем модуль на конкретном теге v5.3.0 через параметр ?ref=
    source = "github.com/Azure/terraform-azurerm-network?ref=5.3.0"

    resource_group_name = azurerm_resource_group.rg.name
    address_space       = "10.0.0.0/16"
    subnet_prefixes     = ["10.0.1.0/24"]
    subnet_names        = ["subnet1"]
    
    # Помнишь нашу ошибку? Не забудь передать этот обязательный аргумент
    use_for_each        = false 
    depends_on = [ azurerm_resource_group.rg ]
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
        # subnet_id                     = module.network.subnet_id
        subnet_id                     = module.network.vnet_subnets[0]
        private_ip_address_allocation = "Dynamic"
        public_ip_address_id          = azurerm_public_ip.pip.id
    }
}

# resource "azurerm_network_interface_security_group_association" "nic_assoc" {
#     network_interface_id      = azurerm_network_interface.nic.id
#     network_security_group_id = module.network.nsg_id
# }

# Генерация временного SSH-ключа, чтобы не мучиться с паролями
resource "tls_private_key" "ssh_key" {
    algorithm = "RSA"
    rsa_bits  = 4096
}

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

    # # Оставляем чистый дефолтный Nginx, чтобы провиженеры могли его заменить
    # custom_data = base64encode(<<-EOF
    #     #!/bin/bash
    #     apt-get update && apt-get install -y nginx
    # EOF
    # )

    # # БЛОК CONNECTION — необходим для работы file и remote-exec
    # connection {
    #     type        = "ssh"
    #     user        = var.admin_username
    #     private_key = tls_private_key.ssh_key.private_key_pem
    #     host        = azurerm_public_ip.pip.ip_address
    # }

    # # СПОСОБ 2: Передача файла по SSH во временную папку VM
    # provisioner "file" {
    #     source      = "index.html"
    #     destination = "/tmp/index.html"
    # }

    # # СПОСОБ 2.5: remote-exec переносит файл и перезапускает веб-сервер
    # provisioner "remote-exec" {
    #     inline = [
    #     "cloud-init status --wait", # Ждем, пока облако достроит машину
    #     "sudo mv /tmp/index.html /var/www/html/index.html",
    #     "sudo systemctl restart nginx"
    #     ]
    # }

    # # ДОБАВЛЯЕМ local-exec: Пишет отчет на твой MacBook
    # provisioner "local-exec" {
    #     command = <<-EOT
    #     echo "VM Name: ${self.name}" > created-vm-info.txt
    #     echo "Public IP: ${azurerm_public_ip.pip.ip_address}" >> created-vm-info.txt
    #     echo "Nginx URL: http://${azurerm_public_ip.pip.ip_address}" >> created-vm-info.txt
    #     echo "Launch Date: $(date)" >> created-vm-info.txt
    #     echo "Created by local-exec." >> created-vm-info.txt
    #     EOT
    # }
}