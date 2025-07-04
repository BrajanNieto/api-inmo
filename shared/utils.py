import json
import decimal
from datetime import datetime, timezone
import boto3

# Recurso DynamoDB compartido
dynamodb = boto3.resource("dynamodb")

def parse_body(event):
    """Devuelve un dict incluso si el body llega como string JSON"""
    if event.get("body") is None:
        return {}
    if isinstance(event["body"], dict):
        return event["body"]
    return json.loads(event["body"])

def now_timestamp():
    """Timestamp UTC actual en segundos (int)"""
    return int(datetime.now(tz=timezone.utc).timestamp())

# ———— Soporte para serializar decimal.Decimal ————

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            # Entero si no tiene parte fraccionaria, float si la tiene
            return int(obj) if obj % 1 == 0 else float(obj)
        return super().default(obj)

def dumps(obj):
    """
    Atajo para json.dumps que usa DecimalEncoder,
    para que DynamoDB-decimals se conviertan bien.
    """
    return json.dumps(obj, cls=DecimalEncoder)
