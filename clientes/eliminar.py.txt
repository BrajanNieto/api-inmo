import json
from shared.utils import dynamodb, parse_body
TABLE = dynamodb.Table("clientes")

def lambda_handler(event, context):
    body = parse_body(event)
    uuid_ = body["uuid"]

    TABLE.delete_item(Key={"uuid": uuid_})
    return {"statusCode": 200, "body": json.dumps({"msg": "Cliente eliminado"})}
