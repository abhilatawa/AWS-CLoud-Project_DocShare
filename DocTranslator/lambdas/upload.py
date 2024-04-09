import boto3
import json
import os


s3_client = boto3.client("s3")
sqs_client = boto3.client("sqs")

bucket_name = os.getenv("S3_BUCKET_NAME")
sqs_queue_url = os.getenv("SQS_NAME")


def lambda_handler(event, context):
    try:
        if "body" not in event or not event["body"]:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "No file provided"}),
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Access-Control-Allow-Methods": "POST",
                },
            }

        # # Extract filename from Content-Disposition header
        # headers = event.get("headers", {})
        # content_disposition = headers.get("Content-Disposition", "")
        # filename = None
        # if content_disposition:
        #     # Extract filename from the Content-Disposition header
        #     filename = content_disposition.split("filename=")[1].strip('"')

        # if not filename:
        #     return {
        #         "statusCode": 400,
        #         "body": json.dumps({"error": "Filename not found in headers"}),
        #         "headers": {
        #             "Content-Type": "application/json",
        #             "Access-Control-Allow-Origin": "*",
        #             "Access-Control-Allow-Headers": "Content-Type",
        #             "Access-Control-Allow-Methods": "POST",
        #         },
        #     }

        filename = "DesignSmells.xlsx"

        # Retrieve file content from event directly (assuming binary data)

        file_content = event["body"]
        # filename = event["body"]["fileName"]

        # form = multipart.parse_form_data(event["body"])
        # file_content = form.files["file"].file.read()
        # filename = form.files["file"].filename

        # Upload file to S3 bucket
        s3_client.put_object(Bucket=bucket_name, Key=filename, Body=file_content)

        # Generate pre-signed URL for the uploaded file
        file_url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": filename},
            ExpiresIn=3600,
        )

        # Construct message body
        message_body = {"url": file_url}

        # Send message to SQS queue
        response = sqs_client.send_message(
            QueueUrl=sqs_queue_url, MessageBody=json.dumps(message_body)
        )

        print("Message sent to SQS queue:", response)

        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "success": "File uploaded to S3 bucket successfully and URL sent to SQS",
                    "public_url": file_url,
                }
            ),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "POST",
            },
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "POST",
            },

        }
