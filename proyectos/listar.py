import json
from shared.utils import dynamodb
TABLE = dynamodb.Table("proyectos")

def lambda_handler(event, context):
    response = TABLE.scan()
    return {"statusCode": 200, "body": json.dumps(response.get("Items", []))}
