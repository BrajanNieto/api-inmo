import json
from shared.utils import dynamodb

TABLE = dynamodb.Table("clientes")

def lambda_handler(event, context):
    items = []
    # Scan paginado para evitar timeouts en tablas grandes
    response = TABLE.scan()
    items.extend(response.get("Items", []))
    while "LastEvaluatedKey" in response:
        response = TABLE.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
        items.extend(response.get("Items", []))

    return {"statusCode": 200,
            "body": json.dumps(items)}
