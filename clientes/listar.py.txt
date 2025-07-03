import json
from shared.utils import dynamodb
TABLE = dynamodb.Table("clientes")

def lambda_handler(event, context):
    """
    Devuelve la lista completa de clientes.
    Usa un Scan ya que la cardinalidad es manejable.
    """
    response = TABLE.scan()
    items = response.get("Items", [])
    return {"statusCode": 200, "body": json.dumps(items)}
