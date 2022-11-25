resource "azurerm_kubernetes_cluster" "aks" {
    name                = "${random_pet.prefix.id}-aks"
    location            = azurerm_resource_group.matrix_rg.location
    resource_group_name = azurerm_resource_group.matrix_rg.name
    dns_prefix          = "${random_pet.prefix.id}-k8s"

    default_node_pool {
        name            = "demo"
        node_count      = 2
        vm_size         = "Standard_B2s"
        os_disk_size_gb = 30
    }

    service_principal {
        client_id     = "${azuread_service_principal.matrix_sp.application_id}"
        client_secret = "${azuread_service_principal_password.matrix_sp_pass.value}"
    }

    role_based_access_control_enabled = true

    tags = {
        environment = var.env
    }

    depends_on = [
        azurerm_container_registry.acr,
        null_resource.docker_push_cli,
        null_resource.docker_push_svr
    ]
}

resource "azurerm_role_assignment" "matrix_aks_assignment" {
    scope                = "${azurerm_kubernetes_cluster.aks.id}"
    role_definition_name = "Contributor"
    principal_id         = "${azuread_service_principal.matrix_sp.object_id}"
}

resource "null_resource" "aks_deploy_cli" {
    provisioner "local-exec" {
    command = <<-EOT
        az aks get-credentials -g ${azurerm_resource_group.matrix_rg.name} -n ${azurerm_kubernetes_cluster.aks.name}
        kubectl create deployment --image=${azurerm_container_registry.acr.login_server}/${var.docker_cli} matrix-cli
    EOT
    }
}

resource "null_resource" "aks_deploy_svr" {
    provisioner "local-exec" {
    command = <<-EOT
        az aks get-credentials -g ${azurerm_resource_group.matrix_rg.name} -n ${azurerm_kubernetes_cluster.aks.name}
        kubectl create deployment --image=${azurerm_container_registry.acr.login_server}/${var.docker_svr} matrix-svr --replicas=8
    EOT
    }
}


