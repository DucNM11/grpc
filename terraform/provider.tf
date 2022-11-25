terraform {
    required_providers {
    azurerm = {
        source  = "hashicorp/azurerm"
        version = "=3.32.0"
    }
    azuread = {
        source = "hashicorp/azuread"
        version = "2.30.0"
    }

    random = {
        source = "hashicorp/random"
        version = "3.4.3"
    }
}
}

# Configure the Microsoft Azure Provider
provider "azurerm" {
    features {}
}

resource "random_pet" "prefix" {}
resource "random_id" "prefix" {
    byte_length = 8
}