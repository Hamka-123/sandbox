output "storage_account_name" {
  value = azurerm_storage_account.alina_storage_account.name
}

output "storage_info" {
  value = {
    id            = azurerm_storage_account.alina_storage_account.id
    tier          = azurerm_storage_account.alina_storage_account.account_tier
    kind          = azurerm_storage_account.alina_storage_account.account_kind
    network_rules = azurerm_storage_account.alina_storage_account.network_rules
  }
}
output "all_storage_details" {
  value     = azurerm_storage_account.alina_storage_account
  sensitive = true
}
# Outputs:

# all_storage_details = <sensitive>
# storage_account_name = "saalinawren"
# storage_info = {
#   "id" = "/subscriptions/7a016bad-eb8a-41c2-acc2-af1d1d8ee11f/resourceGroups/resource_group_alina_wren/providers/Microsoft.Storage/storageAccounts/saalinawren"
#   "kind" = "StorageV2"
#   "network_rules" = tolist([])
#   "tier" = "Standard"
# }

# Вывести all_storage_details красивым json
# terraform output -json all_storage_details | jq
# terraform output -json all_storage_details > sa_info.json  Сохранить в файл
# jq . sa_info.json > sa_info_pretty.json.  Красиво отформатировать и пересохранить json в другой файл

output "test" {
  value = var.users[0]
}
output "test2" {
  value = var.tags["env"]
}
# Вывод данных (Output)
# Нужен, чтобы получить важные данные после деплоя (например, IP сервера) и использовать их в скриптах или просто видеть в консоли.
# output "vm_public_ip" {
#     value       = azurerm_public_ip.main.ip_address
#     description = "Внешний IP адрес нашего сервера"
# }