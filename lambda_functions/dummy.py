import json
import boto3
import datetime
from json import JSONDecodeError
import uuid

session_id = str(uuid.uuid4())

lex_client = boto3.client("lexv2-runtime")


def lambda_handler(event, context):
    # Check if messages are in the event and if the first message contains 'unstructured' with 'text'
    if (
        "messages" in event
        and len(event["messages"]) > 0
        and "unstructured" in event["messages"][0]
        and "text" in event["messages"][0]["unstructured"]
    ):
        user_message = event["messages"][0]["unstructured"]["text"]
        response = lex_client.recognize_text(
            botId="VEO07ZG2RX",
            botAliasId="TSTALIASID",
            localeId="en_US",
            sessionId=session_id,
            text=user_message,
        )
        bot_response = response["messages"][0]["content"]

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
                                "text": bot_response,
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
