import boto3
from boto3.dynamodb.conditions import Key
from os import getenv
from uuid import uuid4
import json

region_name = getenv('APP_REGION')
todos_table = boto3.resource('dynamodb', region_name=region_name ).Table('Todo2024')

def lambda_handler(event, context):
    # we just want to pass simple json and not use aws api lambda proxy integration, which is what we do normally on our own
    # however, when deploying as SAM app - this function receives the proxy integration automatically, so i have to check for it and fool it if it does
    #AWS PROXY REQUEST
    if ( ("body" in event) ):
        event = json.loads(event["body"])

    id = event['id']
    person_id = event["person_id"]
    description = event["description"]
    completed = event['completed']
    
    if "id" is not event or id is None:
        response(400, "Id is required")

    todo = todos_table.get_item(Key={"Id":id})["Item"]
    
    if todo is None:
        response(404, "TODO not found")
    
    if description is not None:
        todo['description'] = description
        
    if completed is not None:
        todo['completed'] = completed

    todos_table.put_item(Item=todo)
    return response(200, todo)


def response(code, body):
    return {
        "statusCode": code,
        "headers": {
            "Content-Type": "application/json"
            },
        "body": json.dumps(body),
        "isBase64Encoded": False
    }