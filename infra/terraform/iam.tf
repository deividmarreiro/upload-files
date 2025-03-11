resource "aws_sns_topic_policy" "files_to_process_policy" {
  arn    = aws_sns_topic.files_to_process_topic.arn
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = { Service = "s3.amazonaws.com" }
        Action    = "SNS:Publish"
        Resource  = aws_sns_topic.files_to_process_topic.arn
        Condition = {
          ArnLike = {
            "aws:SourceArn" = aws_s3_bucket.files_to_process.arn
          }
        }
      }
    ]
  })
}
