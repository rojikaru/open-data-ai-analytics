terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "analytics" {
  name     = "analytics-rg"
  location = var.location
}

resource "azurerm_virtual_network" "analytics" {
  name                = "analytics-vnet"
  location            = azurerm_resource_group.analytics.location
  resource_group_name = azurerm_resource_group.analytics.name
  address_space       = ["10.0.0.0/16"]
}

resource "azurerm_subnet" "analytics" {
  name                 = "analytics-subnet"
  resource_group_name  = azurerm_resource_group.analytics.name
  virtual_network_name = azurerm_virtual_network.analytics.name
  address_prefixes     = ["10.0.1.0/24"]
}

resource "azurerm_public_ip" "analytics" {
  name                = "analytics-pip"
  location            = azurerm_resource_group.analytics.location
  resource_group_name = azurerm_resource_group.analytics.name
  allocation_method   = "Static"
}

resource "azurerm_network_security_group" "analytics" {
  name                = "analytics-nsg"
  location            = azurerm_resource_group.analytics.location
  resource_group_name = azurerm_resource_group.analytics.name

  security_rule {
    name                       = "allow-ssh"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  security_rule {
    name                       = "allow-web"
    priority                   = 110
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = tostring(var.web_port)
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}

resource "azurerm_network_interface" "analytics" {
  name                = "analytics-nic"
  location            = azurerm_resource_group.analytics.location
  resource_group_name = azurerm_resource_group.analytics.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.analytics.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.analytics.id
  }
}

resource "azurerm_network_interface_security_group_association" "analytics" {
  network_interface_id      = azurerm_network_interface.analytics.id
  network_security_group_id = azurerm_network_security_group.analytics.id
}

resource "azurerm_linux_virtual_machine" "analytics" {
  name                = "analytics-vm"
  location            = azurerm_resource_group.analytics.location
  resource_group_name = azurerm_resource_group.analytics.name
  size                = var.vm_size
  admin_username      = var.admin_username

  network_interface_ids = [azurerm_network_interface.analytics.id]

  admin_ssh_key {
    username   = var.admin_username
    public_key = var.admin_ssh_public_key
  }

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-noble"
    sku       = "24_04-lts"
    version   = "latest"
  }

  priority        = "Spot"
  eviction_policy = "Deallocate"
  max_bid_price   = -1

  custom_data = base64encode(templatefile("${path.module}/cloud-init.yaml.tpl", {
    repo_url       = var.repo_url
    admin_username = var.admin_username
    web_port       = var.web_port
  }))
}
