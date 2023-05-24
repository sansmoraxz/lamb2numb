"""Lambda handler function entry point"""

import io
import os

import boto3
import numpy as np

from lamb2numb import hello

# # pylint: disable=unused-argument
def lambda_handler(event, context):
    """
    Lambda handler function
    Parameters
    ----------
    event: dict, required
        S3 put event
        Event doc: https://docs.aws.amazon.com/lambda/latest/dg/with-s3.html
    context: object, required
        Lambda Context runtime methods and attributes
        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html
    """
    # Create an S3 client
    s3_client = boto3.client('s3')
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    hello_s = hello.hello_fn()
    print(hello_s)
    obj = s3_client.get_object(Bucket=bucket_name, Key=key)
    queue_url = os.environ['QUEUE_URL']
    # read s3-object to np array
    with io.BytesIO(obj['Body'].read()) as file_bytes:
        arr = np.load(file_bytes)
        print("Array from S3: ", arr)
        # publish to sqs
        sqs_client = boto3.client('sqs')
        sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=str(arr.tolist())
        )
        return arr