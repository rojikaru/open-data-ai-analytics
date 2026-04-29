output "public_ip_address" {
  description = "Public IP address of the analytics VM"
  value       = aws_eip.analytics.public_ip
}

output "app_url" {
  description = "URL of the web dashboard"
  value       = "http://${aws_eip.analytics.public_ip}:${var.web_port}"
}

output "ssh_command" {
  description = "SSH command to connect to the VM"
  value       = "ssh ${var.admin_username}@${aws_eip.analytics.public_ip}"
}
