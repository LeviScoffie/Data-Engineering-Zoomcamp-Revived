terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.27.0"
    }
  }
}

provider "google" {
  # Configuration options
  project = "optimal-tide-455508-g4"
  region  = "me-west1"
}

resource "google_storage_bucket" "demo-bucket" {
  name          = "optimal-tide-455508-g4-terra-bucket"
  location      = "me-west1"
  force_destroy = true


  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}