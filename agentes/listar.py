import json
from shared.utils import dynamodb
TABLE = dynamodb.Table("agentes")

def lambda_handler(event, context):
    response = TABLE.scan()
    return {"statusCode": 200, "body": json.dumps(response.get("Items", []))}
