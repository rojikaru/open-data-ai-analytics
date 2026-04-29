variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "eu-central-1"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3a.small"
}

variable "admin_username" {
  description = "Linux admin username"
  type        = string
  default     = "ubuntu"
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
  description = "SSH public key content (paste output of: cat ~/.ssh/id_ed25519.pub)"
  type        = string
}
