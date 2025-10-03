import json
from dataclasses import dataclass
import datetime



@dataclass
class RoutePointDC:
    id: int
    route_point_name: str
    route_point_short_name: str
    svg_point: json
    created_time: datetime
    edited_time: datetime
    x_cord: float
    y_cord: float
    z_cord: float
    object_id: int
    point_type_id: int

@dataclass
class ObjectTypeDC:
    id: int
    parent_id: int | None
    object_type_name: str
    object_type_short_name: str
    description_object_type: str | None

@dataclass
class ObjectDrawingDC:
    id: int
    parent_id: int | None
    object_drawing_name: str
    object_drawing_short_name: str
    object_ref: str
    plan_ref: str
    drawing_scale: float
    height: float
    created_time: datetime
    edited_time: datetime
    creator_id: int
    editor_id: int
    object_type_id: int

@dataclass
class ObjectDC:
    id: int
    parent_id: int | None
    object_name: str
    object_short_name: str
    svg_object: json
    created_time: datetime
    edited_time: datetime
    object_status_id: int
    object_drawing_id: int
    object_type_id: int

@dataclass
class PointTypeDC:
    id: int
    point_name: str
    point_short_name: str
    description: str

@dataclass
class ObjectStatusDC:
    id: int
    object_status_name: str


@dataclass
class PointConnectionDC:
    id: int
    route_point1_id: int
    route_point2_id: int
    route_distance: float
    route_time: float
    weight_coefficient: float
    direction_1_to_2: int
    direction_2_to_1: int

@dataclass
class RoutePointsDC:
    routes_points: list[RoutePointDC]

@dataclass
class ObjectTypesDC:
    objects_types: list[ObjectTypeDC]


@dataclass
class ObjectDrawingsDC:
    objects_drawings: list[ObjectDrawingDC]


@dataclass
class ObjectsDC:
    objects: list[ObjectDC]

@dataclass
class PointTypesDC:
    points_types: list[PointTypeDC]

@dataclass
class ObjectStatusesDC:
    objects_status: list[ObjectStatusDC]

@dataclass
class PointConnectionsDC:
    points_conns: list[PointConnectionDC]