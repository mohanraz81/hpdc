import json,boto3, requests
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
        
awsregion="us-east-1"
CheckoutTableName="checkouttable"
def lambda_handler(event, context):
    try:
        iop={"cart":[
            {"productid":"","price":"","productname":""}
            ],
            "address":{},
            "user":"",
            "paymentoption":{}
        }
        
        dynamodb=boto3.resource('dynamodb',region_name=awsregion)
        checkoutdb=dynamodb.Table(CheckoutTableName)
        user = event['user']
        usercart=checkoutdb.get_item(Key={"user":user})
        if 'Item' not in usercart:
            usercart={"user":user,
                      "address":event['address'],
                      "paymentoption":event['paymentoption'],
                      "cart":event['cart'],
                      "status":"initiated"
            }
            
        else:
            usercart=usercart['Item']
        for prod in event['cart']:
            if prod not in usercart['cart']:
                usercart['cart'].append(prod)
        total=0
        for prod in usercart['cart']:
            total=total+int(prod['price'])
        usercart['total']=total
        checkoutdb.put_item(Item=usercart)
        successmessage={
          "status": 200,
          "statusmessage": "Order Placed",
          "total":total
        }
        return(successmessage)
    
    except Exception as e:
        return {"errorMessage":str(e)}