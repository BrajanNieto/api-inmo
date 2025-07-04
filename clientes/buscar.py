import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr
from shared.utils import dynamodb, parse_body, dumps

TABLE = dynamodb.Table("clientes")

def lambda_handler(event, context):
    # 1) Define tus headers CORS
    cors_headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST,OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }

    # 2) Preflight OPTIONS
    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': cors_headers,
            'body': ''
        }

    # 3) Lógica de POST /clientes/buscar
    body = parse_body(event)

    if "email" not in body:
        return {
            'statusCode': 400,
            'headers': cors_headers,
            'body': dumps({"msg": "email es requerido"})
        }

    email = body["email"].lower()

    try:
        response = TABLE.query(
            IndexName="email-index",
            KeyConditionExpression=Key("email").eq(email)
        )
    except ClientError as e:
        if e.response["Error"]["Code"] == "ValidationException":
            response = TABLE.scan(
                FilterExpression=Attr("email").eq(email)
            )
        else:
            raise

    items = response.get("Items", [])
    if items:
        return {
            'statusCode': 200,
            'headers': cors_headers,
            'body': dumps(items[0])
        }

    return {
        'statusCode': 404,
        'headers': cors_headers,
        'body': dumps({"msg": "Cliente no encontrado"})
    }
