"""Lambda handler function entry point."""

import io
import logging
import os
import typing

import boto3
import numpy as np

from .loaders import auto_loader

if typing.TYPE_CHECKING:
    from mypy_boto3_s3 import S3Client
    from mypy_boto3_s3.type_defs import GetObjectOutputTypeDef
    from mypy_boto3_sqs import SQSClient
    from mypy_boto3_sqs.type_defs import SendMessageResultTypeDef

else:
    SQSClient = boto3.client('sqs')
    S3Client = boto3.client('s3')
    GetObjectOutputTypeDef = dict
    SendMessageResultTypeDef = dict

# # pylint: disable=unused-argument
def lambda_handler(event: dict, context: object) -> np.ndarray:
    """Lambda handler function.

    Reads numpy array from S3, publishes it to SQS.

    Parameters
    ----------
    event: dict, required
        S3 put event
        Event doc: https://docs.aws.amazon.com/lambda/latest/dg/with-s3.html

    context: object, required
        Lambda Context runtime methods and attributes
        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    -------
    numpy.ndarray
        Array refresentation of the S3 object
    """
    # Create an S3 client
    s3_client : S3Client = boto3.client('s3')
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    obj : GetObjectOutputTypeDef = s3_client.get_object(Bucket=bucket_name, Key=key)
    queue_url = os.environ['QUEUE_URL']
    # read s3-object to np array
    with io.BytesIO(obj['Body'].read()) as file_bytes:
        arr = auto_loader(file_bytes, key)
        logging.info('Array from S3: %s', arr)
        # publish to sqs
        sqs_client : SQSClient = boto3.client('sqs')
        resp : SendMessageResultTypeDef = sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=str(arr.tolist()),
        )
        logging.info('Message sent to SQS: %s', resp)
        return arr
