terraform {
    required_version = ">=1.2"
    backend "local" {} # can change from "local" to "gcs" - dedicated gcs bucket
    required_providers {
        google ={
            source="hashicorp/google" # library with module definitions such as the "google_storage_bucket"
        }
    }
}

provider "google" {
    project= var.project
    region=var.region

}

# Data Lake Bucket
#Ref:https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket
resource "google_storage_bucket" "data-lake-bucket" {
  name          = "${local.data_lake_bucket}_${var.project}" #COncat DL bucket and project name
  location      = var.region


  # Optional, but recommended settings:
  storage_class = var.storage_class
  uniform_bucket_level_access = true

  versioning {
    enabled = true

  }

  lifecycle_rule {
     action {
      type = "Delete"
    }
    condition {
      age = 30 //days
    }
  }
  force_destroy = true
}

  

  //IN-progress
#BigqUERY DATASET
  #Ref:https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset
resource "google_bigquery_dataset" "dataset" {
  dataset_id=var.BQ_DATASET
  project=var.project
  location = var.region

}