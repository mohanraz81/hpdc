import json,boto3
import time
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
import aws_xray_sdk
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all
patch_all()
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)
def lambda_handler(event, context):
    try:
      awsregion="us-east-1"
      TableName="producttable"
      dynamodb=boto3.resource('dynamodb',region_name=awsregion)
      table=dynamodb.Table(TableName)
      scan_kwargs = {
            "ProjectionExpression": "id, title, description, image, Price"
        }
      done = False
      start_key = None
      response = table.scan(**scan_kwargs)
      response=json.loads(json.dumps(response,cls=DecimalEncoder))
      successmessage={
          "status": 200,
          "statusmessage": "Added Items", 
          "response": response
      }
      return(successmessage)
    except Exception as e:
        return {"errorMessage":str(e)}