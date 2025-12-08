# Monitoring and logging for finance-tracker infrastructure

# CloudWatch dashboard for S3 bucket metrics
resource "aws_cloudwatch_dashboard" "finance_dashboard" {
  dashboard_name = "finance-tracker-dashboard"

  dashboard_body = jsonencode({
    widgets = [
      {
        "type" : "metric",
        "x" : 0,
        "y" : 0,
        "width" : 12,
        "height" : 6,
        "properties" : {
          "title" : "S3 Bucket Size (StandardStorage)",
          "metrics" : [
            [
              "AWS/S3",
              "BucketSizeBytes",
              "BucketName",
              aws_s3_bucket.finance_logs.bucket,
              "StorageType",
              "StandardStorage"
            ]
          ],
          "stat" : "Average",
          "period" : 86400,
          "region" : var.aws_region
        }
      },
      {
        "type" : "metric",
        "x" : 0,
        "y" : 6,
        "width" : 12,
        "height" : 6,
        "properties" : {
          "title" : "S3 All Requests",
          "metrics" : [
            [
              "AWS/S3",
              "AllRequests",
              "BucketName",
              aws_s3_bucket.finance_logs.bucket
            ]
          ],
          "stat" : "Sum",
          "period" : 300,
          "region" : var.aws_region
        }
      }
    ]
  })
}

# Alarm to detect S3 4xx errors (helps troubleshoot access/deployment issues)
resource "aws_cloudwatch_metric_alarm" "s3_4xx_errors" {
  alarm_name          = "finance-tracker-s3-4xx-errors"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 1
  threshold           = 1
  metric_name         = "4xxErrors"
  namespace           = "AWS/S3"
  period              = 300
  statistic           = "Sum"

  dimensions = {
    BucketName = aws_s3_bucket.finance_logs.bucket
  }

  alarm_description = "Alert if S3 bucket is returning 4xx errors (access/config issues)."
}
