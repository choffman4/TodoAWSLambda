import boto3
from boto3.dynamodb.conditions import Key
from os import getenv
from uuid import uuid4
import json

region_name = getenv('APP_REGION')
todos_persons_table = boto3.resource('dynamodb', region_name=region_name ).Table('TodoPerson2024')


def lambda_handler(event, context):
    if "pathParameters" not in event:    
        return response(400, {"error": "no path params"})
    
    path = event["pathParameters"]
    
    if path is None or "id" not in path:
        return response(400, "no id found")
    
    id = path["id"]
    
    #id = "54293035-cac7-4260-844d-bce0637ef07a"
    #id = "8275d4e0-1882-4d7e-9086-b550a91ec6eb"
    
    """ old way of doing it
    if path is not None and "id" in path:
        id = path["id"]
        key = {
            #'IdentityId': identity_id,
            'Id': id
        }
        
    if id is None:
        response(404, "id not found #2")
    
    output = todos_persons_table.delete_item(
        #ConditionExpression=Attr('IdentityId').eq(identity_id) & Attr('Id').eq(id),
        ConditionExpression=Attr('Id').eq(id),
        Key=key
    )
    """
    
    output = todos_persons_table.delete_item(Key={"Id":id})
    
    return response(200, output)
    

def response(code, body):
    return {
        "statusCode": code,
        "headers": {
            "Content-Type": "application/json"
            },
        "body": json.dumps(body),
        "isBase64Encoded": False
    }