resource "google_project_service" "storagetranser"{
  project = var.project
  service= "storagetransfer.googleapis.com"
}



data "google_storage_transfer_project_service_account" "default" {
  project = var.project
}

resource "google_storage_bucket" "transfer-service-terraform-bucket" {
  name          = "transfer-service-terraform-bucket"
  storage_class = "STANDARD"
  project       = var.project
  location      = "EU"
}

resource "google_storage_bucket_iam_member" "transfer-service-terraform-bucket-iam" {
  bucket     = google_storage_bucket.transfer-service-terraform-bucket.name
  role       = "roles/storage.admin"
  member     = "serviceAccount:${data.google_storage_transfer_project_service_account.default.email}"
  depends_on = [google_storage_bucket.transfer-service-terraform-bucket]
}


resource "google_storage_transfer_job" "s3-bucket-nightly-backup3" {
  description = "Execute a cloud transfer job via terraform."
  project     = var.project

  transfer_spec {
    # object_conditions {
    #   max_time_elapsed_since_last_modification = "600s"
    #   exclude_prefixes = [
    #     "requests.gz",
    #   ]
    # }
    transfer_options {
      delete_objects_unique_in_sink = false
    }
    aws_s3_data_source {
      bucket_name = "nyc-tlc"
      aws_access_key {
        access_key_id     = var.access_key_id
        secret_access_key = var.aws_secret_key
      }
    }
    gcs_data_sink {
      bucket_name = google_storage_bucket.transfer-service-terraform-bucket.name
      path        = ""
    }
  }

  schedule {
    schedule_start_date {
      year  = 2022
      month = 10
      day   = 18
    }
    schedule_end_date {
      year  = 2022
      month = 10
      day   = 18
    }
    
  }



  depends_on = [google_storage_bucket_iam_member.transfer-service-terraform-bucket-iam]
}