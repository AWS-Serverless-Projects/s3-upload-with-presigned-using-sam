import json
import boto3
import uuid
import os
from botocore.exceptions import ClientError
from botocore.client import Config

s3 = boto3.client('s3', config=Config(
    signature_version='s3v4',
    s3={'addressing_style': 'virtual'}
    ))


def index(event, context):
    key = str(uuid.uuid4())
    bucket = os.getenv('S3BUCKET')

    try:
        url = s3.generate_presigned_url('put_object',
                                        Params={'Bucket': bucket, 'Key': key},
                                        ExpiresIn=os.getenv('EXPIRY_TIME'),
                                        HttpMethod='PUT',
                                        )

        response = {
            "statusCode": 200,
            "body": json.dumps(url),
            "headers": {
                'Content-Type': 'application/json', 
                'Access-Control-Allow-Origin': '*'
            }
        }
    except ClientError as e:
        print(e)
        response = {
            "statusCode": 500,
            "body": 'Error generating the url'
        }

    return response
