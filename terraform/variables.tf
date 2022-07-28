// public ssh key from GitHub Secrets
variable "ssh_access_key" {
  type = string
}

variable "ssh_key_name" {
  type = string
}

//variable with docker image
variable "backend_docker_image" {
  type = string
}

variable "frontend_docker_image" {
  type = string
}

variable "bot_user_oauth_token" {
  type = string
}

variable "signing_secret" {
  type = string
}

variable "client_secret" {
  type = string
}

variable "db_name" {
  type = string
}

variable "postgres_password" {
  type = string
}

variable "postgres_user" {
  type = string
}

variable "secret_key" {
  type = string
}

variable "docker_token" {
  type = string
}

variable "docker_user" {
  type = string
}

variable "terraform_region" {
  type = string
}
