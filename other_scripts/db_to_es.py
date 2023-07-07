from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3

dynamodb = boto3.resource("dynamodb")
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
region = "us-east-1"
service = "es"
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(
    credentials.access_key,
    credentials.secret_key,
    region,
    service,
    session_token=credentials.token,
)
es = Elasticsearch(
    hosts=[{"host": host, "port": 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
)

mapping = {
    "mappings": {
        "properties": {
            "cuisine_type": {"type": "keyword"},
            "business_id": {"type": "keyword"},
        }
    }
}

if not es.indices.exists("restaurants"):
    es.indices.create(index="restaurants", body=mapping)

for restaurant in restaurants:
    es.index(index="restaurants", body=restaurant)
