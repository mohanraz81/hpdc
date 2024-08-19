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


    # Delete the cart item
    try:
        table.delete_item(
            Key={'userid': user_id}
        )
        response = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps("Item Deleted Successfully"),
        "isBase64Encoded": False
        }
    except Exception as e:
        response = {
            "statusCode": 500,
            "body": json.dumps(f"Error: {str(e)}")
        }

    return response
