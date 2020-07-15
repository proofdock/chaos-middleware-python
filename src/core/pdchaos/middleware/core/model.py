from logzero import logger
from marshmallow import Schema, fields, ValidationError


def parse_paths(config: dict):
    try:
        result = paths_schemas.load(config)

    except ValidationError as x:
        logger.warning("Invalid chaos configuration schema. Reason: {%s}", x)
        result = []

    return result


def parse_attack(header: str):
    try:
        result = attack_schemas.loads(header)

    except ValidationError:
        logger.warning("Invalid attack request. Skipping attack.")
        result = []

    return result


class AttackSchema(Schema):
    class Meta:
        fields = ("probability", "type", "value")

    type = fields.String(required=True)
    value = fields.String(required=True)
    probability = fields.String(required=False)


class PathSchema(Schema):
    class Meta:
        fields = ["path", "attacks", "methods"]

    path = fields.String(required=True)
    attacks = fields.Nested("AttackSchema", required=True, many=True)
    methods = fields.List(fields.String, required=False, many=True)


class PathsSchema(Schema):
    class Meta:
        fields = ["paths"]

    paths = fields.Nested("PathSchema", many=True)


paths_schemas = PathsSchema(many=False)
attack_schemas = AttackSchema(many=True)
