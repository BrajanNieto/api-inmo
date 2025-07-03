import json, uuid
from shared.utils import dynamodb, parse_body
TABLE = dynamodb.Table("proyectos")

def lambda_handler(event, context):
    body = parse_body(event)
    # Si no envían id, generamos uno al vuelo
    body.setdefault("id", str(uuid.uuid4())[:8])
    TABLE.put_item(Item=body)
    return {"statusCode": 200, "body": json.dumps(body)}
