import json, uuid
from shared.utils import dynamodb, parse_body
TABLE = dynamodb.Table("agentes")

def lambda_handler(event, context):
    body = parse_body(event)
    body.setdefault("uuid", str(uuid.uuid4()))
    body.setdefault("active_clients", 0)
    TABLE.put_item(Item=body)
    return {"statusCode": 200, "body": json.dumps(body)}
