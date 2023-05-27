"""Test AWS Lambda handler function."""

import io
import os
import unittest

import boto3
import botocore
import numpy as np
from moto import mock_s3, mock_sqs

from lamb2numb.lambda_handler import lambda_handler

BUCKET_NAME = 'aws-test-bucket-us-esat-145-234'
FILE_NAME = 'my-array.npy'
ARR_SIZE = 1E2
QUEUE_NAME = 'my-queue-123-567-2434'

event = {
    'Records': [
        {
            's3': {
                'bucket': {
                    'name': BUCKET_NAME,
                },
                'object': {
                    'key': FILE_NAME,
                },
            },
        },
    ],
}


def create_s3_bucket(bucket_name: str) -> str:
    """Create S3 bucket.

    Parameters
    ----------
        bucket_name: str
            Bucket name

    Returns
    -------
        str: Bucket name
    """
    print(f'Creating bucket {bucket_name}')
    client = boto3.client('s3')
    try:
        s3resource = boto3.resource('s3')
        s3resource.meta.client.head_bucket(Bucket=bucket_name)
    except botocore.exceptions.ClientError:
        pass
    else:
        msg = f'{bucket_name} should not exist.'
        raise OSError(msg)
    client.create_bucket(Bucket=bucket_name)
    print(f'Bucket {bucket_name} created')
    return bucket_name


def create_sqs_queue(queue_name: str) -> str:
    """Create SQS queue.

    Parameters
    ----------
        queue_name: str, required
            Queue name

    Returns
    -------
        str: Queue URL

    """
    client = boto3.client('sqs')
    response = client.create_queue(
        QueueName=queue_name,
    )
    return response['QueueUrl']


def upload_dummy_array_to_s3(client, bucket_name, file_name):
    """Upload dummy numpy array to S3 bucket.

    Parameters
    ----------
        client: S3Client
            S3 client
        bucket_name: str
            Bucket name
        file_name: str
            File name

    Returns
    -------
        None
    """
    print(f'Uploading dummy array to {bucket_name}/{file_name}')
    array = np.arange(stop=ARR_SIZE)
    buffer = io.BytesIO()
    np.save(buffer, array)
    # IMPORTANT: Reset buffer position to start before uploading
    buffer.seek(0)
    client.put_object(Bucket=bucket_name, Key=file_name, Body=buffer)
    print(f'Uploaded dummy array to {bucket_name}/{file_name}')


@mock_s3
@mock_sqs
class TestAWSLambdaHandler(unittest.TestCase):
    """Test AWS Lambda handler function."""

    def setUp(self):
        """Set up the test fixture before exercising it.

        1. Create S3 bucket
        2. Upload dummy array to S3 bucket
        3. Create SQS queue
        4. Set environment variables
        """
        os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
        create_s3_bucket(BUCKET_NAME)
        client = boto3.client('s3')
        upload_dummy_array_to_s3(client, BUCKET_NAME, FILE_NAME)
        queue_url = create_sqs_queue(QUEUE_NAME)
        os.environ['QUEUE_URL'] = queue_url

    def test_created_object_exists(self):
        """Test that the created object exists."""
        client = boto3.client('s3')
        response = client.list_objects_v2(Bucket=BUCKET_NAME)
        assert 'Contents' in response
        assert len(response['Contents']) == 1
        assert response['Contents'][0]['Key'] == FILE_NAME
        print('Test passed')

    def test_lambda_handler(self):
        """Test lambda_handler."""
        arr = lambda_handler(event, None)
        print('Test returned array')
        assert arr.shape == (int(ARR_SIZE),)
        print('Test SQS message')
        sqs_client = boto3.client('sqs')
        response = sqs_client.receive_message(
            QueueUrl=os.environ['QUEUE_URL'],
        )
        print(response)
        assert 'Messages' in response
        assert len(response['Messages']) == 1
        assert response['Messages'][0]['Body'] == str(arr.tolist())
        print('Response body from SQS:', response['Messages'][0]['Body'])
        print('Test passed')

    def tearDown(self) -> None:
        """Tear down method.

        1. Delete all objects in bucket
        2. Delete bucket.
        """
        s3_client = boto3.client('s3')
        # Delete all objects in bucket
        print(f'Deleting all objects in {BUCKET_NAME}')
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
        if 'Contents' in response:
            for obj in response['Contents']:
                s3_client.delete_object(Bucket=BUCKET_NAME, Key=obj['Key'])
        # Delete bucket
        print(f'Deleting bucket {BUCKET_NAME}')
        s3_client.delete_bucket(Bucket=BUCKET_NAME)
        # Delete queue
        print(f'Deleting queue {QUEUE_NAME}')
        sqs_client = boto3.client('sqs')
        sqs_client.delete_queue(QueueUrl=os.environ['QUEUE_URL'])
        # Delete environment variable
        del os.environ['QUEUE_URL']
        del os.environ['AWS_DEFAULT_REGION']
