import json
from datetime import datetime, timezone
import boto3

dynamodb = boto3.resource("dynamodb")

def parse_body(event):
    """Devuelve un dict incluso si el body llega como string JSON"""
    if event.get("body") is None:
        return {}
    if isinstance(event["body"], dict):
        return event["body"]
    return json.loads(event["body"])

def now_timestamp():
    return int(datetime.now(tz=timezone.utc).timestamp())
