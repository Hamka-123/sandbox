output "kubecontext_aks" {
  description = "Kubernetes context for AKS cluster"
  value       = "aks-${var.owner}"
}
output "resource_group_name" {
  value = azurerm_resource_group.rg.name
}

output "storage_account_name" {
  value = azurerm_storage_account.store.name
}

output "storage_account_key" {
  value     = azurerm_storage_account.store.primary_access_key
  sensitive = true
}

output "aks_cluster_name" {
  value = azurerm_kubernetes_cluster.aks.name
}

output "aks_get_credentials" {
  value = "az aks get-credentials --resource-group ${azurerm_resource_group.rg.name} --name ${azurerm_kubernetes_cluster.aks.name}"
}

output "velero_install_minikube" {
  value = "velero install --provider azure --plugins velero/velero-plugin-for-microsoft-azure:v1.8.0 --bucket velero --secret-file ./credentials-velero --backup-location-config resourceGroup=${azurerm_resource_group.rg.name},storageAccount=${azurerm_storage_account.store.name},subscriptionId=${data.azurerm_subscription.current.subscription_id},storageAccountKeyEnvVar=AZURE_STORAGE_ACCOUNT_ACCESS_KEY --kubecontext minikube --use-node-agent"
}

output "velero_install_aks" {
  value = "velero install --provider azure --plugins velero/velero-plugin-for-microsoft-azure:v1.8.0 --bucket velero --secret-file ./credentials-velero --backup-location-config resourceGroup=${azurerm_resource_group.rg.name},storageAccount=${azurerm_storage_account.store.name},subscriptionId=${data.azurerm_subscription.current.subscription_id},storageAccountKeyEnvVar=AZURE_STORAGE_ACCOUNT_ACCESS_KEY --kubecontext aks-${var.owner} --use-node-agent"
}

