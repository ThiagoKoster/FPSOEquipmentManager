import marshmallow


class InactivateEquipmentSchema(marshmallow.Schema):
    code = marshmallow.fields.Str()



