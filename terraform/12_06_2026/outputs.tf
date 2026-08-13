output "public_ips" {
  description = "Список публичных IP-адресов ВМ"
  value       = [for ip in azurerm_public_ip.pip : ip.ip_address]
}

output "vm_names" {
  description = "Имена созданных ВМ"
  value       = [for vm in azurerm_linux_virtual_machine.vms : vm.name]
}
