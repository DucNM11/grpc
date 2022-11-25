resource "azurerm_container_registry" "acr" {
    name                = "${random_id.prefix.hex}ACR"
    resource_group_name = azurerm_resource_group.matrix_rg.name
    location            = azurerm_resource_group.matrix_rg.location
    sku                 = "Standard"
    tags = {
        environment = var.env
    }
}

resource "azurerm_role_assignment" "matrix_acr_assignment" {
    scope                = "${azurerm_container_registry.acr.id}"
    role_definition_name = "Contributor"
    principal_id         = "${azuread_service_principal.matrix_sp.object_id}"
}

resource "null_resource" "docker_push_svr" {
    provisioner "local-exec" {
    command = <<-EOT
        echo "${azuread_service_principal_password.matrix_sp_pass.value}" | docker login ${azurerm_container_registry.acr.login_server} -u ${azuread_service_principal.matrix_sp.application_id} --password-stdin
        docker tag ${var.docker_svr} ${azurerm_container_registry.acr.login_server}/${var.docker_svr}
        docker push ${azurerm_container_registry.acr.login_server}/${var.docker_svr}
    EOT
    }
}

resource "null_resource" "docker_push_cli" {
    provisioner "local-exec" {
    command = <<-EOT
        echo "${azuread_service_principal_password.matrix_sp_pass.value}" | docker login ${azurerm_container_registry.acr.login_server} -u ${azuread_service_principal.matrix_sp.application_id} --password-stdin
        docker tag ${var.docker_cli} ${azurerm_container_registry.acr.login_server}/${var.docker_cli}
        docker push ${azurerm_container_registry.acr.login_server}/${var.docker_cli}
    EOT
    }
}
