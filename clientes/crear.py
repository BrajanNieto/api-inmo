import uuid
import json
from shared.utils import dynamodb, parse_body, now_timestamp

TABLE = dynamodb.Table("clientes")

def lambda_handler(event, context):
    # 1) Headers CORS
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

    # 3) Parsear el cuerpo de la petición
    body = parse_body(event)

    # 4) Construir el objeto cliente
    cliente = {
        "uuid": str(uuid.uuid4()),
        "fname": body.get("fname"),
        "lname": body.get("lname"),
        "email": body.get("email", "").lower(),
        "phone": body.get("phone"),
        "document": body.get("document"),
        "person_type": body.get("person_type", "natural"),
        "gender": body.get("gender"),
        "created_at": now_timestamp(),
        "num_interactions": 1,
        "last_interaction_date": now_timestamp(),
        "captation_way_id": 79,
        "captation_way": "web page",
        "publicity_consent": body.get("publicity_consent", False),
        "referred_id": body.get("referred_id"),
        "project_id": body.get("project_id"),
        "price_range": body.get("price_range"),
        "bedrooms": body.get("bedrooms"),
        "message": body.get("message"),
        "last_agent_assigned": body.get("agent_uuid")
    }

    # 5) Guardar en DynamoDB
    TABLE.put_item(Item=cliente)

    # 6) Devolver la respuesta con headers CORS
    return {
        'statusCode': 200,
        'headers': cors_headers,
        'body': json.dumps(cliente)
    }
