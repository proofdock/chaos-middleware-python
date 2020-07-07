from marshmallow import Schema, fields, ValidationError


def parse_attack(header: str):
    try:
        result = attack_schemas.loads(header)

    except ValidationError:
        #  Put a warning logger statement here: "Invalid attack request. Skipping attack."
        result = []

    return result


class AttackSchema(Schema):
    class Meta:
        fields = ("probability", "type", "value")

    type = fields.String(required=True)
    value = fields.String(required=True)
    probability = fields.String(required=False)


attack_schemas = AttackSchema(many=True)
