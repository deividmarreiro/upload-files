resource "aws_sns_topic" "files_to_process_topic" {
  name = "files-to-process-topic"
}

resource "aws_sns_topic" "files_processed_topic" {
  name = "files-processed-topic"
}

resource "aws_sns_topic_subscription" "files_to_process_subscription" {
  topic_arn = aws_sns_topic.files_to_process_topic.arn
  protocol  = "sqs"
  endpoint  = aws_sqs_queue.files_to_process_queue.arn
}

resource "aws_sns_topic_subscription" "files_processed_subscription" {
  topic_arn = aws_sns_topic.files_processed_topic.arn
  protocol  = "sqs"
  endpoint  = aws_sqs_queue.files_processed_queue.arn
}
