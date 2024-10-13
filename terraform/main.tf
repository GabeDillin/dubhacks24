resource "azurerm_resource_group" "TravelAI_group" {
  name = "TravelAI_group"
  location = "westus2"
}

resource "azurerm_storage_account" "storage" {
  name                     = "travelaistorage1"
  resource_group_name       = "TravelAI_group"
  location                  = "westus2"
  account_tier              = "Standard"
  account_replication_type  = "LRS"
}

resource "azurerm_storage_container" "state_container" {
  name                  = "travelai-backend"
  storage_account_name  = azurerm_storage_account.storage.name
  container_access_type = "private"
}

resource "azurerm_static_web_app" "static_site" {
  name                     = "TravelAIapp"
  resource_group_name      = "TravelAI_group"
  location                 = "westus2"
  sku_tier                 = "Standard"
  sku_size                 = "Standard"

  identity {
    type = "SystemAssigned"
  }
}