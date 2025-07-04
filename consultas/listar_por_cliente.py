# consultas/listar_por_cliente.py

from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
from shared.utils import dynamodb, parse_body, dumps

TABLE = dynamodb.Table("consultas")

def lambda_handler(event, context):
    body = parse_body(event)

    # Validación básica
    if "cliente_uuid" not in body:
        return {
            "statusCode": 400,
            "body": dumps({"msg": "cliente_uuid es requerido"})
        }

    cliente_uuid = body["cliente_uuid"]

    # Ejecutar query paginado para todos los ítems de este cliente
    try:
        response = TABLE.query(
            KeyConditionExpression=Key("cliente_uuid").eq(cliente_uuid)
        )
    except ClientError as e:
        # Si hay error de bajo nivel, relanzamos
        raise

    items = response.get("Items", [])

    # Si la consulta devuelve más de 1 000 ítems, seguimos paginando
    while "LastEvaluatedKey" in response:
        response = TABLE.query(
            KeyConditionExpression=Key("cliente_uuid").eq(cliente_uuid),
            ExclusiveStartKey=response["LastEvaluatedKey"]
        )
        items.extend(response.get("Items", []))

    return {
        "statusCode": 200,
        "body": dumps(items)
    }
