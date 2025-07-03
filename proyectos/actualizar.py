import json
from shared.utils import dynamodb, parse_body
TABLE = dynamodb.Table("proyectos")

def lambda_handler(event, context):
    body = parse_body(event)
    proj_id = body.pop("id")   # id no se actualiza, sólo se usa como clave

    # Construimos UpdateExpression dinámico
    update_expr = "SET "
    expr_attr_vals = {}
    for i, (k, v) in enumerate(body.items(), start=1):
        update_expr += f"{k} = :v{i}, "
        expr_attr_vals[f":v{i}"] = v
    update_expr = update_expr.rstrip(", ")

    TABLE.update_item(
        Key={"id": proj_id},
        UpdateExpression=update_expr,
        ExpressionAttributeValues=expr_attr_vals
    )
    return {"statusCode": 200, "body": json.dumps({"msg": "Proyecto actualizado"})}
