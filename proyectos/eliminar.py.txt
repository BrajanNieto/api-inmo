import json
from shared.utils import dynamodb, parse_body
TABLE = dynamodb.Table("proyectos")

def lambda_handler(event, context):
    body = parse_body(event)
    proj_id = body["id"]
    TABLE.delete_item(Key={"id": proj_id})
    return {"statusCode": 200, "body": json.dumps({"msg": "Proyecto eliminado"})}
