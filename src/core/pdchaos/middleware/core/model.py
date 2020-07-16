from marshmallow import Schema, fields


class AttackSchema(Schema):
    class Meta:
        fields = ["action", "probability", "target", "type", "value"]

    action = fields.String(required=True)
    probability = fields.String(required=False)
    target = fields.Nested("TargetSchema", required=False)
    type = fields.String(required=False)
    value = fields.String(required=True)


class TargetSchema(Schema):
    class Meta:
        fields = ["route", "service"]

    route = fields.String(required=False)
    service = fields.String(required=False)


attack_schemas = AttackSchema(many=True)
