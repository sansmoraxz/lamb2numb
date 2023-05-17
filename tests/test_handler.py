"""Test AWS Lambda handler function"""

from src.lambda_handler import lambda_handler


event = {
    "Records": [
        {
            "s3": {
                "bucket": {
                    "name": "aws-test-bucket-ces-df-fv1-234000-us-east-1"
                },
                "object": {
                    "key": "my-array.npy"
                }
            }
        }
    ]
}

def test_lambda_handler():
    """Test lambda_handler
    """
    lambda_handler(event, None)
    assert True
