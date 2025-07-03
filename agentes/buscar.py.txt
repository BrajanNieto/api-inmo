import json
from shared.utils import dynamodb, parse_body
TABLE = dynamodb.Table("agentes")

def lambda_handler(event, context):
    body = parse_body(event)
    uuid_ = body["uuid"]

    resp = TABLE.get_item(Key={"uuid": uuid_})
    if "Item" in resp:
        return {"statusCode": 200, "body": json.dumps(resp["Item"])}
    return {"statusCode": 404, "body": json.dumps({"msg": "Agente no encontrado"})}
