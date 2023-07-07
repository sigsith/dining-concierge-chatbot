import json
import boto3

ses = boto3.client("ses")


def lambda_handler(event, context):
    for record in event["Records"]:
        slots = json.loads(record["body"])
        print(slots)  # print the slots here
        cuisine = slots["Cuisine"]["value"]["originalValue"]
        dining_time = slots["DiningTime"]["value"]["originalValue"]
        email = slots["Email"]["value"]["originalValue"]
        location_city = slots["LocationCity"]["value"]["originalValue"]
        num_people = slots["NumPeople"]["value"]["originalValue"]
        message = f"Cuisine: {cuisine}\nLocation: {location_city}\nNumber of people: {num_people}\nDining Time: {dining_time}"
        subject = "Your restaurant recommendation details"
        send_email(email, subject, message)
    return {"statusCode": 200, "body": json.dumps("Hello from Lambda!")}


def send_email(email, subject, body):
    ses.send_email(
        Source="jeff@aws.com",
        Destination={
            "ToAddresses": [
                email,
            ]
        },
        Message={
            "Subject": {
                "Data": subject,
            },
            "Body": {
                "Text": {
                    "Data": body,
                }
            },
        },
    )
