import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr
from shared.utils import dynamodb, parse_body, dumps

TABLE = dynamodb.Table("clientes")

def lambda_handler(event, context):
    body = parse_body(event)

    # Validación básica
    if "email" not in body:
        return {
            "statusCode": 400,
            "body": dumps({"msg": "email es requerido"})
        }

    email = body["email"].lower()

    # Intentamos usar el GSI 'email-index'
    try:
        response = TABLE.query(
            IndexName="email-index",
            KeyConditionExpression=Key("email").eq(email)
        )
    except ClientError as e:
        # Si realmente no existe el índice, hacemos fallback a scan con Attr
        if e.response["Error"]["Code"] == "ValidationException":
            response = TABLE.scan(
                FilterExpression=Attr("email").eq(email)
            )
        else:
            # Para cualquier otro error, lo re-lanzamos
            raise

    items = response.get("Items", [])
    if items:
        return {
            "statusCode": 200,
            "body": dumps(items[0])
        }

    return {
        "statusCode": 404,
        "body": dumps({"msg": "Cliente no encontrado"})
    }
