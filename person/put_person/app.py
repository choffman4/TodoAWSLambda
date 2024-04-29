import boto3
from boto3.dynamodb.conditions import Key
from os import getenv
from uuid import uuid4
import json

region_name = getenv('APP_REGION')
todos_persons_table = boto3.resource('dynamodb', region_name=region_name ).Table('TodoPerson2024')

def lambda_handler(event, context):
    # we just want to pass simple json and not use aws api lambda proxy integration, which is what we do normally on our own
    # however, when deploying as SAM app - this function receives the proxy integration automatically, so i have to check for it and fool it if it does
    #AWS PROXY REQUEST
    if ( ("body" in event) ):
        event = json.loads(event["body"])

    id = event['id']
    name = event['name']
    email = event['email']
    password = event['password']
    
    if "id" is not event or id is None:
        response(400, "Id is required")

    person = todos_persons_table.get_item(Key={"Id":id})["Item"]
    
    if person is None:
        response(404, "Person not found")
    
    if name is not None:
        person['name'] = name
        
    if email is not None:
        person['email'] = email
        
    if password is not None:
        person['password'] = password


    todos_persons_table.put_item(Item=person)
    return response(200, person)


def response(code, body):
    return {
        "statusCode": code,
        "headers": {
            "Content-Type": "application/json"
            },
        "body": json.dumps(body),
        "isBase64Encoded": False
    }