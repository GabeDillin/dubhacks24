terraform {
  backend "azurerm" {
    resource_group_name   = "TravelAI_group"
    storage_account_name  = "TravelAI_storage"
    container_name        = "TravelAI_backend"
    key                   = "terraform.tfstate"
  }

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "4.4.0"
    }
  }
}

provider "azurerm" {
  features {}
  client_id = "66cd24ef-652d-433d-943c-c825d08b5b35"
  client_secret = "wx68Q~K5QAhmzjB3jRFRMYKyjYAaq2XzEwXkIbsn"
  subscription_id = "b33030cc-2e15-41ef-b05a-1f9762ac6665"
  tenant_id = "ad01d2bf-bf41-4ac3-ad98-dc0cce30f7e9"
}