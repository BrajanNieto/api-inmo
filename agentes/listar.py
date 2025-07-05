# agentes/listar.py

from shared.utils import dynamodb, dumps

TABLE = dynamodb.Table("agentes")

def lambda_handler(event, context):
    # 1) Headers CORS
    cors_headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET,OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }

    # 2) Preflight OPTIONS
    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': cors_headers,
            'body': ''
        }

    # 3) GET /agentes/listar
    items = []
    response = TABLE.scan()
    items.extend(response.get("Items", []))
    while "LastEvaluatedKey" in response:
        response = TABLE.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
        items.extend(response.get("Items", []))

    # 4) Responde con los headers CORS + el body JSON
    return {
        'statusCode': 200,
        'headers': cors_headers,
        'body': dumps(items)
    }
