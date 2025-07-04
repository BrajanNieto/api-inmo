# proyectos/listar.py

from shared.utils import dynamodb, dumps

TABLE = dynamodb.Table("proyectos")

def lambda_handler(event, context):
    items = []
    # Scan paginado para evitar timeouts en tablas grandes
    response = TABLE.scan()
    items.extend(response.get("Items", []))

    while "LastEvaluatedKey" in response:
        response = TABLE.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
        items.extend(response.get("Items", []))

    return {
        "statusCode": 200,
        "body": dumps(items)
    }
