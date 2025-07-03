import json
from shared.utils import dynamodb, parse_body
TABLE = dynamodb.Table("proyectos")

def lambda_handler(event, context):
    body = parse_body(event)
    proj_id = body["id"]

    resp = TABLE.get_item(Key={"id": proj_id})
    if "Item" in resp:
        return {"statusCode": 200, "body": json.dumps(resp["Item"])}
    return {"statusCode": 404, "body": json.dumps({"msg": "Proyecto no encontrado"})}
