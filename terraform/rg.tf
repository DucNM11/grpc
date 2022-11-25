resource "azurerm_resource_group" "matrix_rg" {
    name              = "${random_pet.prefix.id}-aks-rg"
    location          = "UK South"
    tags = {
        environment = var.env
    }
}
