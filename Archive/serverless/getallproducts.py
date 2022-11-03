import json,boto3,decimal



class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)
        
        
awsregion="us-east-1"
TableName="producttable"


dynamodb=boto3.resource('dynamodb',region_name=awsregion)
table=dynamodb.Table(TableName)

  
def lambda_handler(event, context):
  scan_kwargs = {
        "ProjectionExpression": "id, title, description, image, Price"
    }
  response = table.scan(**scan_kwargs)
  response=json.loads(json.dumps(response,cls=DecimalEncoder))
  successmessage={
      "status": 200,
      "statusmessage": "Added Items", 
      "response": response
  }
  print(successmessage)
  return(successmessage)