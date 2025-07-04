# proyectos/buscar.py
from botocore.exceptions import ClientError
from shared.utils import dynamodb, parse_body, dumps

TABLE = dynamodb.Table("proyectos")

def lambda_handler(event, context):
    # Parsear el body y validar entrada
    body = parse_body(event)
    if "id" not in body:
        return {
            "statusCode": 400,
            "body": dumps({"msg": "id es requerido"})
        }

    proj_id = body["id"]
    try:
        # Obtener el item por clave primaria
        response = TABLE.get_item(Key={"id": proj_id})
    except ClientError:
        # Propagar otros errores de cliente
        raise

    item = response.get("Item")
    if item:
        return {
            "statusCode": 200,
            "body": dumps(item)
        }

    # Si no existe el proyecto
    return {
        "statusCode": 404,
        "body": dumps({"msg": "Proyecto no encontrado"})
    }
