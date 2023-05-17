"""Test AWS Lambda handler function"""

import io
import unittest

from moto import mock_s3
import boto3
import botocore

import numpy as np

from src.lambda_handler import lambda_handler


BUCKET_NAME = 'aws-test-bucket-ces-df-fv1-234000-us-east-13'
FILE_NAME = 'my-array.npy'
ARR_SIZE = 1E6

event = {
    "Records": [
        {
            "s3": {
                "bucket": {
                    "name": BUCKET_NAME
                },
                "object": {
                    "key": FILE_NAME
                }
            }
        }
    ]
}

def create_s3_bucket(bucket_name):
    """Create S3 bucket

    Args:
        bucket_name (str): Bucket name
    """
    print(f"Creating bucket {bucket_name}")
    client = boto3.client("s3")
    try:
        s3resource = boto3.resource("s3")
        s3resource.meta.client.head_bucket(Bucket=bucket_name)
    except botocore.exceptions.ClientError:
        pass
    else:
        raise EnvironmentError(f"{bucket_name} should not exist.")
    client.create_bucket(Bucket=bucket_name)
    print(f"Bucket {bucket_name} created")


def upload_dummy_array_to_s3(client, bucket_name, file_name):
    """Upload dummy numpy array to S3 bucket

    Args:
        client (boto3.client): S3 client
        bucket_name (str): Bucket name
        file_name (str): File name
    """

    print(f"Uploading dummy array to {bucket_name}/{file_name}")
    array = np.arange(stop=1E6)
    buffer = io.BytesIO()
    np.save(buffer, array)
    # IMPORTANT: Reset buffer position to start before uploading
    buffer.seek(0)
    client.put_object(Bucket=bucket_name, Key=file_name, Body=buffer)
    print(f"Uploaded dummy array to {bucket_name}/{file_name}")


@mock_s3
class TestAWSLambdaHandler(unittest.TestCase):
    """Test AWS Lambda handler function"""
    def setUp(self):
        """Setup method
            1. Create mock S3 bucket
            2. Upload dummy numpy array to S3 bucket
        """
        create_s3_bucket(BUCKET_NAME)
        client = boto3.client("s3")
        upload_dummy_array_to_s3(client, BUCKET_NAME, FILE_NAME)

    def test_created_object_exists(self):
        """Test that the created object exists"""
        client = boto3.client("s3")
        response = client.list_objects_v2(Bucket=BUCKET_NAME)
        assert 'Contents' in response
        assert len(response['Contents']) == 1
        assert response['Contents'][0]['Key'] == FILE_NAME

    def test_lambda_handler(self):
        """Test lambda_handler"""
        lambda_handler(event, None)
        assert True

    def tearDown(self):
        """Tear down method
            1. Delete all objects in bucket
            2. Delete bucket
        """
        client = boto3.client("s3")
        # Delete all objects in bucket
        print(f"Deleting all objects in {BUCKET_NAME}")
        response = client.list_objects_v2(Bucket=BUCKET_NAME)
        if 'Contents' in response:
            for obj in response['Contents']:
                client.delete_object(Bucket=BUCKET_NAME, Key=obj['Key'])
        # Delete bucket
        print(f"Deleting bucket {BUCKET_NAME}")
        client.delete_bucket(Bucket=BUCKET_NAME)
