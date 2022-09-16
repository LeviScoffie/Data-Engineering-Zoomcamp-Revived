locals {
  data_lake_bucket="dtc_data_lake"
}

variable "project" {
  description = "Your GCP Project ID"
  
#   type= string
}

variable "region" {
    description = "Region for GCP resources.Choose as per your location: https://cloud.google.com/about/locations"
    default="europe-west6"
    type = string
}

#not needed for now
variable "bucket_name" {
    description="The name of the Google Cloud Storage buccket.Must be globally unique"
    default=""
  
}

variable "storage_class" {
    description = "Storage class type for your bucket.More info in docs"
    default = "STANDARD"
}
variable "BQ_DATASET"{ #SCHEMa
    description="BigQuery Dataset that raw data (from GCS) will be written to"
    type = string 
    default = "trips_data_all"
}   

variable "TABLE_NAME" { #can be part of locals
    description = "BigQuery Table"
    type=string
    default = "ny_trips"
  
}
