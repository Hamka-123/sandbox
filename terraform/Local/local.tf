terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "2.7.0"
    }
  }
}

provider "local" {
  # Configuration options
}

resource "local_file" "alina"{
    filename = "alina.txt"
    content = "Alina loves sleep"
    file_permission = "0777"
    
    lifecycle {
      create_before_destroy = true
    }
}


resource "local_file" "alina2"{
    filename = "alina2.txt"
    content = "Alina loves sleep"
    file_permission = "0777"
}