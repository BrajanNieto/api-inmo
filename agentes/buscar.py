# agentes/buscar.py

from botocore.exceptions import ClientError
from shared.utils import dynamodb, parse_body, dumps

TABLE = dynamodb.Table("agentes")

def lambda_handler(event, context):
    body = parse_body(event)

    # Validación básica
    if "uuid" not in body:
        return {
            "statusCode": 400,
            "body": dumps({"msg": "uuid es requerido"})
        }

    uuid_ = body["uuid"]

    # Intentamos obtener el agente por su UUID
    try:
        resp = TABLE.get_item(Key={"uuid": uuid_})
    except ClientError:
        # En caso de error de bajo nivel, relanzamos
        raise

    item = resp.get("Item")
    if item:
        return {
            "statusCode": 200,
            "body": dumps(item)
        }

    return {
        "statusCode": 404,
        "body": dumps({"msg": "Agente no encontrado"})
    }
