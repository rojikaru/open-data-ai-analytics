output "public_ip_address" {
  description = "Public IP address of the analytics VM"
  value       = azurerm_public_ip.analytics.ip_address
}

output "app_url" {
  description = "URL of the web dashboard"
  value       = "http://${azurerm_public_ip.analytics.ip_address}:${var.web_port}"
}
