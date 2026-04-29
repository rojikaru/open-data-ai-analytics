variable "location" {
  description = "Azure region"
  type        = string
  default     = "westeurope"
}

variable "vm_size" {
  description = "Azure VM SKU"
  type        = string
  default     = "Standard_B2ats_v2"
}

variable "admin_username" {
  description = "Linux admin username"
  type        = string
  default     = "azureuser"
}

variable "repo_url" {
  description = "Public GitHub HTTPS URL of the project repository"
  type        = string
}

variable "web_port" {
  description = "Port the web service listens on (must match WEB_PORT in .env)"
  type        = number
  default     = 8000
}

variable "admin_ssh_public_key" {
  description = "RSA SSH public key content (paste output of: cat ~/.ssh/id_rsa.pub)"
  type        = string
}
