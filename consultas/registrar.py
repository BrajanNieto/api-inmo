import uuid, json
from shared.utils import dynamodb, parse_body, now_timestamp
TABLE = dynamodb.Table("consultas")

def lambda_handler(event, context):
    body = parse_body(event)

    consulta = {
        "id": str(uuid.uuid4()),
        "cliente_uuid": body["cliente_uuid"],
        "fecha": now_timestamp(),
        "proyecto_id": body["proyecto_id"],
        "mensaje": body["message"],
        "rango_precio": body["price_range"],
        "dormitorios": body["bedrooms"],
        "canal": "web page",
        "agente_asignado": body.get("agent_uuid"),
        "publicity_consent": body.get("publicity_consent", False),
        "referred_id": body.get("referred_id")
    }

    TABLE.put_item(Item=consulta)
    return {"statusCode": 200, "body": json.dumps(consulta)}
