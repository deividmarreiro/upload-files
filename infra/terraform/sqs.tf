resource "aws_sqs_queue" "files_to_process_queue" {
  name = "files-to-process"
}

resource "aws_sqs_queue" "files_processed_queue" {
  name = "files-processed"
}