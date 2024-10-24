terraform {
  backend "azurerm" {
    resource_group_name   = "TravelAI_group"
    storage_account_name  = "travelaistorage1"
    container_name        = "travelai-backend"
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
}
