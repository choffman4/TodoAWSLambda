import boto3
from boto3.dynamodb.conditions import Key
from os import getenv
from uuid import uuid4
import json

region_name = getenv('APP_REGION')
todos_table = boto3.resource('dynamodb', region_name=region_name ).Table('Todo2024')


def lambda_handler(event, context):
    
    #return response(200, event)
    
    if ( ("pathParameters" in event) ):
        
        path = event["pathParameters"]
        
        if path is None or "id" not in path:
            #return response(200, "no id found, return all")
            return response(200, todos_table.scan()["Items"])
            
        if path is not None and "id" in path:
            id = path["id"]
            output = todos_table.get_item(Key={"Id":id})["Item"]
            return response(200, output)

    # for some reason, no path paramaters got passed, so we just return everything anyway
    return response(200, todos_table.scan()["Items"])

    #output = todos_persons_table.get_item(Key={"Id":"54293035-cac7-4260-844d-bce0637ef07a"})["Item"]
    #return response(200, output)


def response(code, body):
    return {
        "statusCode": code,
        "headers": {
            "Content-Type": "application/json"
            },
        "body": json.dumps(body),
        "isBase64Encoded": False
    }