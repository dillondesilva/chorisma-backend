from botocore.config import Config

import boto3
import json
import shortuuid

s3_client = boto3.client("s3", region_name="ap-southeast-2", config=Config(signature_version='s3v4'))

def lambda_handler(event, context):
    key = f"listened_chords/{shortuuid.uuid()}"
    url = s3_client.generate_presigned_url(
        ClientMethod='put_object',
        Params={'Bucket': "chorisma-app", 'Key': key},
        ExpiresIn=10000
    )

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Origin": "*", 
            "Access-Control-Allow-Methods": "GET"
        },
        "body": json.dumps({
            "preSignedURL": url,
            "key": key
        })
    }