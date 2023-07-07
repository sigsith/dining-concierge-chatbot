import json
import boto3
import datetime
from json import JSONDecodeError


def lambda_handler(event, context):
    try:
        body = json.loads(event["body"])
        message = body["messages"][0]["unstructured"]["text"]
        # if everything goes well, respond with the message received
        response_message = "Received: " + message
    except (json.JSONDecodeError, KeyError):
        # if something goes wrong, respond with an error message
        response_message = "Request body is missing or malformed"

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(
            {
                "messages": [
                    {
                        "type": "response",
                        "unstructured": {
                            "id": "1",
                            "text": response_message,
                            "timestamp": str(datetime.datetime.now()),
                        },
                    }
                ]
            }
        ),
    }
