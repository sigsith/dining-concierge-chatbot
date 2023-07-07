import json
import boto3
import datetime
import uuid

session_id = str(uuid.uuid4())

lex_client = boto3.client("lexv2-runtime")


def lambda_handler(event, context):
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
        messages = response.get("messages", [])
        bot_responses = [
            {
                "type": "response",
                "unstructured": {
                    "id": str(i + 1),
                    "text": msg.get("content", ""),
                    "timestamp": str(datetime.datetime.now()),
                },
            }
            for i, msg in enumerate(messages)
        ]

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps({"messages": bot_responses}),
        }
    else:
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps({"error": "Invalid request format"}),
        }
