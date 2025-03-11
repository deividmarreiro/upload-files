resource "aws_s3_bucket" "files_to_process" {
  bucket = "files-to-process"
}

resource "aws_s3_bucket" "files_processed" {
  bucket = "files-processed"
}

