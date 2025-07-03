import json
from shared.utils import dynamodb, parse_body, now_timestamp
TABLE = dynamodb.Table("clientes")

def lambda_handler(event, context):
    body = parse_body(event)
    uuid_ = body["uuid"]

    update_expr = "SET #ni = if_not_exists(num_interactions, :zero) + :one, last_interaction_date = :now"
    expr_attr_names = {"#ni": "num_interactions"}
    expr_attr_vals = {":one": 1, ":zero": 0, ":now": now_timestamp()}

    # puedes agregar más campos a actualizar individualmente:
    for campo in ["phone", "price_range", "bedrooms", "message"]:
        if campo in body:
            update_expr += f", {campo} = :{campo}"
            expr_attr_vals[f":{campo}"] = body[campo]

    TABLE.update_item(
        Key={"uuid": uuid_},
        UpdateExpression=update_expr,
        ExpressionAttributeNames=expr_attr_names,
        ExpressionAttributeValues=expr_attr_vals
    )
    return {"statusCode": 200, "body": json.dumps({"msg": "Cliente actualizado"})}
