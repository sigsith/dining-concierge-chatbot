import json
import boto3
import datetime
import uuid

session_id = str(uuid.uuid4())
lex_client = boto3.client("lexv2-runtime")
sqs = boto3.client("sqs")


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
        sessionState = response.get("sessionState", {})
        if sessionState is not None:
            send_slots(sessionState)
        messages = response.get("messages", [])
        if messages is not None:
            return pack_up(messages)
        else:
            return error("No message returned")
    else:
        return error("Invalid request format")


def send_slots(sessionState):
    intent = sessionState.get("intent", {})
    if intent is None:
        return
    if (
        intent["name"] == "DiningSuggestion"
        and intent["state"] == "ReadyForFulfillment"
    ):
        slots = intent["slots"]
        if not check_filled(slots):
            return
        sqs.send_message(
            QueueUrl="https://sqs.us-east-1.amazonaws.com/466369883393/UserRequest",
            MessageBody=json.dumps(slots),
        )


def check_filled(slots):
    for value in slots.values():
        if value is None:
            return False
    return True


def pack_up(messages):
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


def error(message):
    return {
        "statusCode": 400,
        "headers": {
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps({"error": message}),
    }
