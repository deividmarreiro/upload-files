resource "aws_s3_bucket_notification" "files_to_process_event" {
  bucket = aws_s3_bucket.files_to_process.bucket

  topic {
    events    = ["s3:ObjectCreated:*"]
    topic_arn = aws_sns_topic.files_to_process_topic.arn
    filter_prefix = "input/"
    
  }
}

resource "aws_s3_bucket_notification" "files_processed_event" {
  bucket = aws_s3_bucket.files_processed.bucket

  topic {
    events    = ["s3:ObjectCreated:*"]
    topic_arn = aws_sns_topic.files_processed_topic.arn
    filter_prefix = "input/"
    
  }
}
