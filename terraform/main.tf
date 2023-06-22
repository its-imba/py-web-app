# Boilerplate template - needs configuring
# Define Azure provider and authentication
provider "azurerm" {
  features {}
}

# Define resource group
resource "azurerm_resource_group" "example" {
  name     = "<resource_group_name>"
  location = "<location>"
}

# Define virtual network
resource "azurerm_virtual_network" "example" {
  name                = "<virtual_network_name>"
  address_space       = ["<address_space_cidr_block>"]
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
}

# Define subnet within the virtual network
resource "azurerm_subnet" "example" {
  name                 = "<subnet_name>"
  address_prefixes     = ["<subnet_cidr_block>"]
  resource_group_name  = azurerm_resource_group.example.name
  virtual_network_name = azurerm_virtual_network.example.name
}

# Define network security group
resource "azurerm_network_security_group" "example" {
  name                = "<network_security_group_name>"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name

  security_rule {
    name                       = "Allow-SSH"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}

# Define network interface
resource "azurerm_network_interface" "example" {
  name                      = "<network_interface_name>"
  location                  = azurerm_resource_group.example.location
  resource_group_name       = azurerm_resource_group.example.name
  network_security_group_id = azurerm_network_security_group.example.id

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.example.id
    private_ip_address_allocation = "Dynamic"
  }
}

# Define virtual machine
resource "azurerm_virtual_machine" "example" {
  name                  = "<virtual_machine_name>"
  location              = azurerm_resource_group.example.location
  resource_group_name   = azurerm_resource_group.example.name
  network_interface_ids = [azurerm_network_interface.example.id]
  vm_size               = "<vm_size>"

  storage_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }

  storage_os_disk {
    name              = "osdisk"
    caching           = "ReadWrite"
    create_option     = "FromImage"
    managed_disk_type = "Standard_LRS"
  }

  os_profile {
    computer_name  = "<computer_name>"
    admin_username = "<admin_username>"
    admin_password = "<admin_password>"
  }

  os_profile_linux_config {
    disable_password_authentication = false
  }

  boot_diagnostics {
    enabled     = true
    storage_uri = azurerm_storage_account.example.primary_blob_endpoint
  }
}

# Define storage account for boot diagnostics
resource "azurerm_storage_account" "example" {
  name                     = "<storage_account_name>"
  resource_group_name      = azurerm_resource_group.example.name
  location                 = azurerm_resource_group.example.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  network_rules {
    default_action = "Deny"
    ip_rules       = ["<your_ip_address>"]
  }
}
