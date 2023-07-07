import json
import boto3
import datetime
from json import JSONDecodeError


def lambda_handler(event, context):
    # Check if messages are in the event and if the first message contains 'unstructured' with 'text'
    if (
        "messages" in event
        and len(event["messages"]) > 0
        and "unstructured" in event["messages"][0]
        and "text" in event["messages"][0]["unstructured"]
    ):
        user_message = event["messages"][0]["unstructured"]["text"]
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
                                "text": f"Received message: {user_message}",
                                "timestamp": str(datetime.datetime.now()),
                            },
                        }
                    ]
                }
            ),
        }
    else:
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps({"error": "Invalid request format"}),
        }
