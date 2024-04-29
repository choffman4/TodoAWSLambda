import boto3
from boto3.dynamodb.conditions import Key
from os import getenv
from uuid import uuid4
import json
from datetime import datetime

region_name = getenv('APP_REGION')
todos_persons_table = boto3.resource('dynamodb', region_name=region_name ).Table('Todo2024')


def lambda_handler(event, context):
    # we just want to pass simple json and not use aws api lambda proxy integration, which is what we do normally on our own
    # however, when deploying as SAM app - this function receives the proxy integration automatically, so i have to check for it and fool it if it does
    #AWS PROXY REQUEST
    if ( ("body" in event) ):
        event = json.loads(event["body"])
    
    todo_id = str(uuid4())
    person_id = event["person_id"]
    description = event["description"]
    date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
    completed = False
    
    
    todos_persons_table.put_item(Item={
        'Id': todo_id,
        'person_id' : person_id,
        'description' : description,
        'date' : date,
        'completed' : completed
    })
    
    return response(200, {"Id": todo_id})
    
def response(code, body):
    return {
        "statusCode": code,
        "headers": {
            "Content-Type": "application/json"
            },
        "body": json.dumps(body),
        "isBase64Encoded": False
    }