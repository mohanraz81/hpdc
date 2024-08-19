import json
import boto3
def lambda_handler(event, context):
    # Extract request data from the event
    print(event)
    # user_id = event['userid']
    # cart_items = event['cartitems']
    TableName = 'carttable'
    dynamodb=boto3.resource('dynamodb',region_name='us-east-1')
    table=dynamodb.Table(TableName)
    # Update the user's cart in DynamoDB

    response=table.put_item(Item=json.loads(event['body']))
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Cart updated successfully'}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
    else:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error'}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }