import json
from shared.utils import dynamodb, parse_body
TABLE = dynamodb.Table("agentes")

def lambda_handler(event, context):
    body = parse_body(event)
    uuid_ = body.pop("uuid")

    update_expr = "SET "
    expr_attr_vals = {}
    for i, (k, v) in enumerate(body.items(), start=1):
        update_expr += f"{k} = :v{i}, "
        expr_attr_vals[f":v{i}"] = v
    update_expr = update_expr.rstrip(", ")

    TABLE.update_item(
        Key={"uuid": uuid_},
        UpdateExpression=update_expr,
        ExpressionAttributeValues=expr_attr_vals
    )
    return {"statusCode": 200, "body": json.dumps({"msg": "Agente actualizado"})}
