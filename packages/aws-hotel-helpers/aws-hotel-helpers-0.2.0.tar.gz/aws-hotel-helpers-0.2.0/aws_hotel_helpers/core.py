# aws_hotel_helpers/core.py
import boto3
from botocore.exceptions import ClientError
import logging
from .exceptions import AWSHelperException
import uuid
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class AWSHelper:
    def __init__(self, region_name='us-east-1', credentials=None):
        self.region_name = region_name
        self._session = None
        self._initialize_session(credentials)
        self.sns_topic_arn = None
        self.sqs_queue_url = None
        
    def _initialize_session(self, credentials):
        try:
            if credentials:
                self._session = boto3.Session(
                    aws_access_key_id=credentials.get('aws_access_key_id'),
                    aws_secret_access_key=credentials.get('aws_secret_access_key'),
                    aws_session_token=credentials.get('aws_session_token'),
                    region_name=self.region_name
                )
            else:
                self._session = boto3.Session(region_name=self.region_name)
            
            # Initialize clients
            self.s3_client = self._session.client('s3')
            self.sns = self._session.client('sns')
            self.sqs = self._session.client('sqs')
            self.dynamodb = self._session.client('dynamodb')
            self.ses = self._session.client('ses')
            
        except Exception as e:
            raise AWSHelperException(f"Failed to initialize AWS session: {str(e)}")

    def upload_to_s3(self, file_obj, key, bucket_name, content_type=None):
        """Upload file to S3"""
        try:
            if hasattr(file_obj, 'seek'):
                file_obj.seek(0)
            
            content_type = content_type or getattr(file_obj, 'content_type', 'image/jpeg')
            logger.info(f"Uploading to S3: {key} ({content_type})")
            
            self.s3_client.upload_fileobj(
                file_obj,
                bucket_name,
                key,
                ExtraArgs={'ContentType': content_type}
            )
            
            # Verify upload
            self.s3_client.head_object(
                Bucket=bucket_name,
                Key=key
            )
            
            # Generate presigned URL
            url = self.get_presigned_url(bucket_name, key)
            logger.info(f"File uploaded successfully. URL: {url}")
            return url
            
        except Exception as e:
            raise AWSHelperException(f"Failed to upload to S3: {str(e)}")

    def get_presigned_url(self, bucket_name, key, expiration=3600):
        """Generate a presigned URL for an S3 object"""
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': bucket_name,
                    'Key': key
                },
                ExpiresIn=expiration
            )
            return url
        except Exception as e:
            raise AWSHelperException(f"Failed to generate presigned URL: {str(e)}")

    def send_booking_confirmation(self, booking_data):
        """Send booking confirmation via SNS and email"""
        try:
            # Format message
            message = f"""
            Booking Confirmation
            
            Thank you for booking with us!
            
            Booking Details:
            Hotel: {booking_data['hotel_name']}
            Room: {booking_data['room_type']}
            Check-in: {booking_data['check_in']}
            Check-out: {booking_data['check_out']}
            Total Price: ${booking_data['total_price']}
            
            Booking Reference: {booking_data['booking_id']}
            """
            
            # Send via SNS
            if self.sns_topic_arn:
                self.sns.publish(
                    TopicArn=self.sns_topic_arn,
                    Message=message,
                    Subject='Booking Confirmation'
                )
            
            # Send via SES if configured
            if booking_data.get('user_email'):
                self.send_email_notification(
                    booking_data['user_email'],
                    'Booking Confirmation',
                    message
                )
            
            return True
            
        except Exception as e:
            raise AWSHelperException(f"Failed to send booking confirmation: {str(e)}")

    def send_email_notification(self, email, subject, message, sender_email=None):
        """Send email via SES"""
        try:
            self.ses.send_email(
                Source=sender_email or 'noreply@yourdomain.com',
                Destination={'ToAddresses': [email]},
                Message={
                    'Subject': {'Data': subject},
                    'Body': {'Text': {'Data': message}}
                }
            )
            logger.info(f"Email sent to {email}")
            return True
        except Exception as e:
            raise AWSHelperException(f"Failed to send email: {str(e)}")

    def send_to_sqs(self, queue_url, message_body):
        """Send message to SQS queue"""
        try:
            response = self.sqs.send_message(
                QueueUrl=queue_url,
                MessageBody=json.dumps(message_body)
            )
            return response['MessageId']
        except Exception as e:
            raise AWSHelperException(f"Failed to send SQS message: {str(e)}")

    def receive_from_sqs(self, queue_url, max_messages=10):
        """Receive messages from SQS queue"""
        try:
            response = self.sqs.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=max_messages,
                WaitTimeSeconds=5
            )
            return response.get('Messages', [])
        except Exception as e:
            raise AWSHelperException(f"Failed to receive SQS messages: {str(e)}")

    def save_to_dynamodb(self, table_name, item):
        """Save item to DynamoDB table"""
        try:
            self.dynamodb.put_item(
                TableName=table_name,
                Item=item
            )
            return True
        except Exception as e:
            raise AWSHelperException(f"Failed to save to DynamoDB: {str(e)}")