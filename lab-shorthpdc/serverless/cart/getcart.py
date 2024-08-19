import json
import boto3
import decimal
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)
def lambda_handler(event, context):
    #print(event)
    #Parse the input data from the event
    user_id = event['queryStringParameters']['userid']

    # Initialize the DynamoDB client
    dynamodb = boto3.resource('dynamodb')
    table_name = 'carttable'
    table = dynamodb.Table(table_name)

    # Query DynamoDB to get cart items for the user
# Query the table for items where the UserId matches the provided UserId

    output = table.get_item(Key={"userid": user_id})
    outputjson = json.loads(json.dumps(output,cls=DecimalEncoder))
    

    if 'Item' in outputjson:
        response = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(outputjson['Item']),
        "isBase64Encoded": False
        }
    else:
        response = {
            "status": 404,
            "body": "Cart is empty for this user."
        }
    return response