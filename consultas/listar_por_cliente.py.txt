import json
from boto3.dynamodb.conditions import Key
from shared.utils import dynamodb, parse_body
TABLE = dynamodb.Table("consultas")

def lambda_handler(event, context):
    body = parse_body(event)
    cliente_uuid = body["cliente_uuid"]

    response = TABLE.query(
        KeyConditionExpression=Key("cliente_uuid").eq(cliente_uuid)
    )
    return {"statusCode": 200, "body": json.dumps(response.get("Items", []))}
