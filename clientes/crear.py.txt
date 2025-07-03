import uuid, json
from shared.utils import dynamodb, parse_body, now_timestamp
TABLE = dynamodb.Table("clientes")

def lambda_handler(event, context):
    body = parse_body(event)
    cliente = {
        "uuid": str(uuid.uuid4()),
        "fname": body["fname"],
        "lname": body["lname"],
        "email": body["email"].lower(),
        "phone": body["phone"],
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
        "project_id": body["project_id"],      # link al proyecto elegido
        "price_range": body["price_range"],
        "bedrooms": body["bedrooms"],
        "message": body["message"],
        "last_agent_assigned": body.get("agent_uuid"),  # agente pre-asignado opcional
    }

    TABLE.put_item(Item=cliente)
    return {"statusCode": 200, "body": json.dumps(cliente)}
