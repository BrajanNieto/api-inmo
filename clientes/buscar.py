import json
from shared.utils import dynamodb, parse_body
TABLE = dynamodb.Table("clientes")

def lambda_handler(event, context):
    body = parse_body(event)
    email = body["email"].lower()

    # buscar por GSI email-index
    response = TABLE.query(
        IndexName="email-index",
        KeyConditionExpression=boto3.dynamodb.conditions.Key("email").eq(email)
    )
    if response["Items"]:
        return {"statusCode": 200, "body": json.dumps(response["Items"][0])}
    return {"statusCode": 404, "body": json.dumps({"msg": "Cliente no encontrado"})}

