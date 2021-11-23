import json

def index(event, context):
    print(event)
    return {
        "statusCode": 202,
        "body": json.dumps(event)
    }
