import requests
import boto3
import time
from datetime import datetime

# create a session
session = boto3.Session()

# create a resource for dynamodb
dynamodb = session.resource("dynamodb")

# table reference
table = dynamodb.Table("yelp-restaurants")

# Yelp API Key
api_key = "your_yelp_api_key"
headers = {"Authorization": "Bearer %s" % api_key}

# list of cuisines. Should map one to one to Lex custom CousineType.
cuisines = [
    "Chinese",
    "Mexican",
    "Asian",
    "Korean",
    "Thai",
    "Indian",
    "Vegan",
    "Italian",
    "Salad",
    "Seafood",
    "Breakfast",
    "Pizza",
    "Burgers",
    "Steakhouses",
    "Sandwiches",
    "Vietnamese",
    "American",
]

for cuisine in cuisines:
    url = (
        "https://api.yelp.com/v3/businesses/search?location=Manhattan&term="
        + cuisine
        + "+restaurants"
    )
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        businesses = response.json()["businesses"]

        for business in businesses:
            item = {
                "Business ID": business["id"],
                "Name": business["name"],
                "Address": " ".join(business["location"]["display_address"]),
                "Coordinates": business["coordinates"],
                "Number of Reviews": business["review_count"],
                "Rating": business["rating"],
                "Zip Code": business["location"]["zip_code"],
                "insertedAtTimestamp": datetime.now().isoformat(),
            }

            # insert the item into dynamodb
            table.put_item(Item=item)

            time.sleep(1)  # To prevent exceeding Yelp API's rate limits
    else:
        print(f"Request failed with status code {response.status_code}")
