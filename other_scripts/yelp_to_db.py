import requests
import boto3
import time
from datetime import datetime
from decimal import Decimal

# create a session
session = boto3.Session(region_name="us-east-1")

# create a resource for dynamodb
dynamodb = session.resource("dynamodb")

# table reference
table = dynamodb.Table("yelp-restaurants")

# Yelp API Key
api_key = "kiki"
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
    counter = 0
    print(f"Getting data for {cuisine}")
    for offset in range(0, 1200, 50):
        url = (
            "https://api.yelp.com/v3/businesses/search?location=Manhattan&term="
            + cuisine
            + "+restaurants"
            + f"&limit=50&offset={offset}"
        )
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            businesses = response.json()["businesses"]
            print(f"Received {len(businesses)} businesses for {cuisine}")
            for business in businesses:
                counter += 1
                if counter > 1000:
                    break
                item = {
                    "Business ID": business["id"],
                    "Name": business["name"],
                    "Cuisine Type": cuisine,
                    "Address": " ".join(business["location"]["display_address"]),
                    "Coordinates": {
                        "latitude": Decimal(str(business["coordinates"]["latitude"])),
                        "longitude": Decimal(str(business["coordinates"]["longitude"])),
                    },
                    "Number of Reviews": business["review_count"],
                    "Rating": Decimal(str(business["rating"])),
                    "Zip Code": business["location"]["zip_code"],
                    "insertedAtTimestamp": datetime.now().isoformat(),
                }
                print(f"Inserting item {counter} for {cuisine}")
                # insert the item into dynamodb
                try:
                    table.put_item(Item=item)
                    print(f"Successfully inserted item {counter} for {cuisine}")
                except Exception as e:
                    print(f"Failed to insert item {counter} for {cuisine}. Error: {e}")

        else:
            print(f"Request failed with status code {response.status_code}")
        time.sleep(1)
