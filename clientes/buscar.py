import json
import boto3                               # ❶  Faltaba
from boto3.dynamodb.conditions import Key  # ❷
from shared.utils import dynamodb, parse_body

TABLE = dynamodb.Table("clientes")

def lambda_handler(event, context):
    body = parse_body(event)

    # Validación básica
    if "email" not in body:
        return {"statusCode": 400,
                "body": json.dumps({"msg": "email es requerido"})}

    email = body["email"].lower()

    # ❸  Usa el índice secundario 'email-index'
    try:
        response = TABLE.query(
            IndexName="email-index",
            KeyConditionExpression=Key("email").eq(email)
        )
    except TABLE.meta.client.exceptions.ResourceNotFoundException:
        # El índice no existe: usa scan como respaldo
        response = TABLE.scan(
            FilterExpression=Key("email").eq(email)
        )

    items = response.get("Items", [])
    if items:
        return {"statusCode": 200,
                "body": json.dumps(items[0])}

    return {"statusCode": 404,
            "body": json.dumps({"msg": "Cliente no encontrado"})}

