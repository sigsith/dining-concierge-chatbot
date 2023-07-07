from elasticsearch import Elasticsearch
import boto3

session = boto3.Session(region_name="us-east-1")
dynamodb = session.resource("dynamodb")
table = dynamodb.Table("yelp-restaurants")
response = table.scan()
restaurants = []
for item in response["Items"]:
    restaurant = {
        "cuisine_type": item["Cuisine Type"],
        "business_id": item["Business ID"],
    }
    restaurants.append(restaurant)

host = "https://search-restaurants-es-wegtnplh3c565avrppxyu57ury.us-east-1.es.amazonaws.com"
es = Elasticsearch(
    hosts=[{"host": host, "port": 443}],
    use_ssl=True,
    verify_certs=True,
)

mapping = {
    "mappings": {
        "properties": {
            "cuisine_type": {"type": "keyword"},
            "business_id": {"type": "keyword"},
        }
    }
}

index_name = "restaurants"

es.indices.create(index=index_name, body=mapping)

actions = []

# Iterate over the restaurants and create index actions for each
for restaurant in restaurants:
    action = {
        "_index": index_name,
        "_source": restaurant,
    }
    actions.append(action)

response = es.bulk(index=index_name, body=actions, refresh=True)

if response["errors"]:
    for item in response["items"]:
        if "error" in item["index"]:
            print(f"Failed to index restaurant: {item['index']['_id']}")
else:
    print("All restaurants indexed successfully.")
