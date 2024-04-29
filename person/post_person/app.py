import boto3
from boto3.dynamodb.conditions import Key
from os import getenv
from uuid import uuid4
import json
from datetime import datetime

region_name = getenv('APP_REGION')
todos_persons_table = boto3.resource('dynamodb', region_name=region_name ).Table('TodoPerson2024')

# never use this, but good example code
#dynamo_client = boto3.resource(service_name="dynamodb", region_name="us-east-2", aws_access_key_id="XXXXXX", aws_secret_access_key="XXXXXXX")


def lambda_handler(event, context):
    # we just want to pass simple json and not use aws api lambda proxy integration, which is what we do normally on our own
    # however, when deploying as SAM app - this function receives the proxy integration automatically, so i have to check for it and fool it if it does
    #AWS PROXY REQUEST
    if ( ("body" in event) ):
        event = json.loads(event["body"])

    person_id = str(uuid4())
    name = event["name"]
    email = event["email"]
    password = event["password"]    
    
    db_insert(person_id, name, email, password)
    
    return response(200, {"Id": person_id, "newstuff": "here WAS HERE"})


# you can talk directly to dynamodb remotely in the cloud
def db_insert(person_id, name, email, password):

    date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')

    todos_persons_table.put_item(Item={
        'Id': person_id,
        'name' : name,
        'email' : email,
        'password' : password,
        'date' : date
    })


def response(code, body):
    return {
        "statusCode": code,
        "headers": {
            "Content-Type": "application/json"
            },
        "body": json.dumps(body),
        "isBase64Encoded": False
    }

"""
my_event = {
  "name": "choffman",
  "password": "abc123",
  "email": "choffman@student.neumont.edu"
}
"""

# lambda_handler(my_event, None)
