import json
import boto3

def lambda_handler(event, context):
    # Parse the input data from the event
    body = json.loads(event['body'])
    user_id = body['userid']
    product_id = body['productId']
    new_quantity = body['quantity']

    # Initialize the DynamoDB client
    dynamodb = boto3.resource('dynamodb')
    table_name = 'carttable'
    table = dynamodb.Table(table_name)

    # Update cart item quantity
    try:
        table.update_item(
            Key={'userid': user_id },
            UpdateExpression="SET quantity = :qty, productId = :pid",
            ExpressionAttributeValues={':qty': new_quantity, ':pid': product_id}
        )
        response = {
            "statusCode": 200,
            "body": json.dumps("Cart item quantity updated successfully.")
        }
    except Exception as e:
        response = {
            "statusCode": 500,
            "body": json.dumps(f"Error: {str(e)}")
        }

    return response