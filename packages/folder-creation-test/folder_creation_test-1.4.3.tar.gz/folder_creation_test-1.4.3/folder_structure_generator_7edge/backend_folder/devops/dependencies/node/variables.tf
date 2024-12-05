variable "STAGE" {
  type        = string
  description = "read from environment variable"
}

variable "REGION" {
  type        = string
  description = "read from environment variable"
}

variable "DOMAIN" {
  type        = string
  description = "read from environment variable"
}

variable "RDS_CLUSTER_PASSWORD" {
  type        = string
  description = "read from environment variable"
}

variable "JWT_SECRET_KEY" {
  type        = string
  description = "read from environment variable"
}

variable "SENDER_EMAIL" {
  type        = string
  description = "read from environment variable"
}

variable "RDS_DATABASE_NAME" {
  type        = string
  description = "read from environment variable"
}
