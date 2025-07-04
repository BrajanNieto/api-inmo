from shared.utils import dynamodb, dumps

TABLE = dynamodb.Table("proyectos")

def lambda_handler(event, context):
    # 1) Define aquí tus headers CORS
    cors_headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET,OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }

    # 2) Si es preflight (OPTIONS), responde solo con headers y status 200
    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': cors_headers,
            'body': ''
        }

    # 3) Para GET, ejecuta tu lógica normal
    items = []
    response = TABLE.scan()
    items.extend(response.get("Items", []))
    while "LastEvaluatedKey" in response:
        response = TABLE.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
        items.extend(response.get("Items", []))

    # 4) Devuelve también los headers CORS junto con el body
    return {
        'statusCode': 200,
        'headers': cors_headers,
        'body': dumps(items)
    }
