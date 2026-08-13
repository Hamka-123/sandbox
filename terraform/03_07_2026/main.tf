

module "server_1" {
  source              = "../modules/vm"
  base_name           = "webserver"
  resource_group_name = module.naming.resource_group.name
  admin_username      = "alya_admin"
}
module "naming" {
  source  = "Azure/naming/azurerm"
  version = "0.4.3"
  suffix  = ["Alina-${terraform.workspace}"]
}



# module "web_server_2" {
#     source = "./modules/compute"
#     name   = "web-server-2"
# }
