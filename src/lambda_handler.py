"""Lambda handler function entry point"""

import io

import boto3
import numpy as np

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
    obj = s3_client.get_object(Bucket=bucket_name, Key=key)
    # read s3-object to np array
    with io.BytesIO(obj['Body'].read()) as file_bytes:
        arr = np.load(file_bytes)
        print("Array from S3: ", arr)
