import json
import datetime


def lambda_handler(event, context):
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
                            "text": "I’m still under development. Please come back later.",
                            "timestamp": str(datetime.datetime.now()),
                        },
                    }
                ]
            }
        ),
    }
