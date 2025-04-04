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
  project = var.project
  region  = var.location
}

resource "google_storage_bucket" "ny-taxi-data-lake" {
  name          = var.gcs_bucket_name
  location      = var.location
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

resource "google_bigquery_dataset" "ny-rides" {
  dataset_id = var.bq_dataset_name
  location = var.location
}