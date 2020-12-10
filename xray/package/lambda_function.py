import json,boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
import aws_xray_sdk
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all
patch_all()
def lambda_handler(event, context):
  try:
    return {"status":200,'body':{}}
  except Exception as e:
    return {"errorMessage":str(e)}
