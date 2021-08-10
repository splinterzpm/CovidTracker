variable "location" {
  default = "West Europe"
}

variable "tags" {
  type = map(string)
  default = { 
    owner = "grigorii_marushov@epam.com"
    }
}

variable "resource_group_name" {
  default = "epm-rdsp"
}