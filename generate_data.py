#!/usr/bin/env python3
import os
import sys

import numpy as np
import boto3


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python generate_data.py <bucket-name>")
        sys.exit(1)
    print("Generating random array...")
    rand_arr = np.random.rand(100, 100)

    OBJ_NAME = "my-array.npy"
    print("Saving to local...")
    np.save(OBJ_NAME, rand_arr)

    print("Uploading to S3...")
    s3_client = boto3.client('s3')
    s3_client.upload_file(OBJ_NAME, sys.argv[1], OBJ_NAME)

    print("Deleting local file...")
    os.remove(OBJ_NAME)

    print("Done!")
