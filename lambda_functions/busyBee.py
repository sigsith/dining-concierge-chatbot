import json
import boto3
from boto3.dynamodb.conditions import Attr
import random

ses = boto3.client("ses")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("yelp-restaurants")


def lambda_handler(event, context):
    for record in event["Records"]:
        slots = json.loads(record["body"])
        cuisine = slots["Cuisine"]["value"]["originalValue"]
        dining_time = slots["DiningTime"]["value"]["originalValue"]
        email = slots["Email"]["value"]["originalValue"]
        location_city = slots["LocationCity"]["value"]["originalValue"]
        num_people = slots["NumPeople"]["value"]["originalValue"]
        restaurant = pick_restaurant(cuisine)
        message = f"Cuisine: {cuisine}\nLocation: {location_city}\nNumber of people: {num_people}\nDining Time: {dining_time}"
        message += f"\n\nRestaurant Suggestion: {restaurant['Name']}\nAddress: {restaurant['Address']}\nNumber of Reviews: {restaurant['Number of Reviews']}\nRating: {restaurant['Rating']}"
        subject = "Your restaurant recommendation details"
        send_email(email, subject, message)
    return {"statusCode": 200, "body": json.dumps("Hello from Lambda!")}


def pick_restaurant(requested_cuisine):
    response = table.scan(FilterExpression=Attr("Cuisine Type").eq(requested_cuisine))
    items = response["Items"]
    # Random is the best algorithm. It's always fair, no fake reviews or monopoly.
    random_restaurant = random.choice(items)
    return random_restaurant


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
