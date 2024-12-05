import boto3
from botocore.exceptions import ClientError
import logging
from .exceptions import AWSHelperException
import uuid
import json

logger = logging.getLogger(__name__)

class AWSHelper:
    """Main class for AWS operations in hotel management systems"""
    
    def __init__(self, region_name='us-east-1', credentials=None):
        """
        Initialize AWS Helper
        
        Args:
            region_name (str): AWS region name (default: 'us-east-1')
            credentials (dict): Optional AWS credentials containing:
                              - aws_access_key_id
                              - aws_secret_access_key
                              - aws_session_token
        """
        self.region_name = region_name
        self._session = None
        self._initialize_session(credentials)
    
    def _initialize_session(self, credentials):
        """Initialize boto3 session with credentials"""
        try:
            if credentials:
                self._session = boto3.Session(
                    aws_access_key_id=credentials.get('aws_access_key_id'),
                    aws_secret_access_key=credentials.get('aws_secret_access_key'),
                    aws_session_token=credentials.get('aws_session_token'),
                    region_name=self.region_name
                )
            else:
                # Use default credentials from environment/instance profile
                self._session = boto3.Session(region_name=self.region_name)
            
            # Verify session by making a simple API call
            sts = self._session.client('sts')
            sts.get_caller_identity()
            
        except Exception as e:
            raise AWSHelperException(f"Failed to initialize AWS session: {str(e)}")
    
    def upload_image(self, image_file, bucket_name, prefix='hotel_images'):
        """
        Upload image to S3 bucket
        
        Args:
            image_file: File object to upload
            bucket_name: S3 bucket name
            prefix: Optional prefix for S3 key (default: 'hotel_images')
            
        Returns:
            str: URL of uploaded image
        
        Raises:
            AWSHelperException: If upload fails
        """
        try:
            s3 = self._session.client('s3')
            
            # Generate unique file name
            file_extension = image_file.name.split('.')[-1].lower()
            file_name = f"{uuid.uuid4()}.{file_extension}"
            key = f"{prefix}/{file_name}"
            
            # Upload file
            s3.upload_fileobj(
                image_file,
                bucket_name,
                key,
                ExtraArgs={'ContentType': image_file.content_type}
            )
            
            # Generate URL
            url = s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket_name, 'Key': key},
                ExpiresIn=3600
            )
            
            return url
            
        except Exception as e:
            raise AWSHelperException(f"Failed to upload image: {str(e)}")
    
    def send_booking_notification(self, topic_arn, booking_data):
        """
        Send booking notification via SNS
        
        Args:
            topic_arn: SNS topic ARN
            booking_data: Dictionary containing booking information
        
        Raises:
            AWSHelperException: If sending notification fails
        """
        try:
            sns = self._session.client('sns')
            
            # Format message
            message = {
                'booking_id': str(booking_data['booking_id']),
                'user_email': booking_data['user_email'],
                'hotel_name': booking_data['hotel_name'],
                'check_in': booking_data['check_in'],
                'check_out': booking_data['check_out'],
                'total_price': str(booking_data['total_price'])
            }
            
            # Send notification
            sns.publish(
                TopicArn=topic_arn,
                Message=json.dumps(message),
                Subject='Booking Confirmation'
            )
            
            logger.info(f"Sent booking notification for booking {booking_data['booking_id']}")
            
        except Exception as e:
            raise AWSHelperException(f"Failed to send notification: {str(e)}")