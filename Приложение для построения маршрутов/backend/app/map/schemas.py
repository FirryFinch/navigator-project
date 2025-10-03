from marshmallow import Schema, fields

class NewObjectDrawingsSchema(Schema):
    parent_id = fields.Int(required=False)
    object_drawing_name = fields.Str(required=True)
    object_drawing_short_name = fields.Str(required=True)
    object_ref = fields.Str(required=True)
    plan_ref = fields.Str(required=True)
    drawing_scale = fields.Float(required=True)
    height = fields.Float(required=True)
    object_type_id = fields.Int(required=True)

class UpdObjectDrawingsSchema(Schema):
    object_drawing_name = fields.Str(required=True)
    object_drawing_short_name = fields.Str(required=True)
    object_ref = fields.Str(required=True)
    plan_ref = fields.Str(required=True)
    drawing_scale = fields.Float(required=True)
    height = fields.Float(required=True)

class NewObjectTypeSchema(Schema):
    parent_id = fields.Int(required=False)
    object_type_name = fields.Str(required=True)
    object_type_short_name = fields.Str(required=True)
    description_object_type = fields.Str(required=False)

class UpdObjecTypeSchema(Schema):
    object_type_name = fields.Str(required=False)
    object_type_short_name = fields.Str(required=False)
    description_object_type = fields.Str(required=False)


class NewRoutePointSchema(Schema):
    route_point_name = fields.Str(required=True)
    route_point_short_name = fields.Str(required=True)
    svg_point = fields.Str(required=True)
    object_id = fields.Int(required=True)
    point_type_id = fields.Int(required=True)
    x = fields.Float(requred=True)
    y = fields.Float(requred=True)
    z = fields.Float(requred=True)



class UpdRoutePointSchema(Schema):
    route_point_name = fields.Str(required=False)
    route_point_short_name = fields.Str(required=False)
    svg_point = fields.Str(required=False)
    x = fields.Float(requred=False)
    y = fields.Float(requred=False)
    z = fields.Float(requred=False)


class NewPointConnSchema(Schema):
    route_point1_id = fields.Int(required=True)
    route_point2_id = fields.Int(required=True)
    route_distance = fields.Float(requred=True)
    route_time = fields.Float(requred=True)
    weight_coefficient = fields.Float(requred=True)
    direction_1_to_2 = fields.Int(required=True)
    direction_2_to_1 = fields.Int(required=True)

class UpdPointConnSchema(Schema):
    route_distance = fields.Float(requred=True)
    route_time = fields.Float(requred=True)
    weight_coefficient = fields.Float(requred=True)
    direction_1_to_2 = fields.Int(required=True)
    direction_2_to_1 = fields.Int(required=True)

class NewObjectStatusSchema(Schema):
    object_status_name = fields.Str(required=True)


class UpdObjectStatusSchema(Schema):
    object_status_name = fields.Str(required=True)

class NewPointTypeSchema(Schema):
    point_name = fields.Str(required=False)
    point_short_name = fields.Str(required=False)
    description = fields.Str(required=False)


class UpdPointTypeSchema(Schema):
    point_name = fields.Str(required=False)
    point_short_name = fields.Str(required=False)
    description = fields.Str(required=False)

class NewObjectSchema(Schema):
    parent_id = fields.Int(required=False)
    object_name = fields.Str(required=True)
    object_short_name = fields.Str(required=True)
    svg_object = fields.Str(required=True)
    object_status_id = fields.Str(required=True)
    object_drawing_id = fields.Float(required=True)
    object_type_id = fields.Float(required=True)


class UpdObjectSchema(Schema):
    object_name = fields.Str(required=True)
    object_short_name = fields.Str(required=True)
    svg_object = fields.Str(required=True)
