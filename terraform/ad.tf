data "azuread_client_config" "current" {}

resource "azuread_application" "matrix_app" {
    display_name = "matrix_app"
    owners       = [data.azuread_client_config.current.object_id]
}

resource "azuread_service_principal" "matrix_sp" {
    application_id = "${azuread_application.matrix_app.application_id}"
}

resource "azuread_service_principal_password" "matrix_sp_pass" {
    service_principal_id = "${azuread_service_principal.matrix_sp.id}"
    end_date_relative    = "8760h"
}
