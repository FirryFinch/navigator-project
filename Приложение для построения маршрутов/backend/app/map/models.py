from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Float,
    DateTime,
    UniqueConstraint, JSON,
)
from sqlalchemy.orm import relationship
from app.base.db import db
from app.map.dataclasses import RoutePointDC, ObjectDC, ObjectDrawingDC, \
    ObjectTypeDC, PointTypeDC, ObjectStatusDC, PointConnectionDC

class PointTypeModel(db):
    __tablename__ = "point_type"

    id = Column(Integer, primary_key=True, autoincrement=True)
    point_name = Column(String, unique=True, nullable=False)
    point_short_name = Column(String, nullable=False)
    description = Column(String, nullable=False)


    route_point = relationship(
        "RoutePointModel", back_populates="point_type", foreign_keys="RoutePointModel.point_type_id"
    )

    def to_dc(self) -> PointTypeDC:
        return PointTypeDC(
            id=self.id,
            point_name=self.point_name,
            point_short_name=self.point_short_name,
            description=self.description,
        )

class ObjectStatusModel(db):
    __tablename__ = "object_status"

    id = Column(Integer, primary_key=True, autoincrement=True)
    object_status_name = Column(String, unique=True, nullable=False)

    object = relationship(
        "ObjectModel", back_populates="object_status", foreign_keys="ObjectModel.object_status_id"
    )

    def to_dc(self) -> ObjectStatusDC:
        return ObjectStatusDC(
            id=self.id,
            object_status_name=self.object_status_name,
        )

class ObjectTypeModel(db):
    __tablename__ = "object_type"

    id = Column(Integer, primary_key=True, autoincrement=True)
    object_type_name = Column(String, unique=True, nullable=False)
    object_type_short_name = Column(String, unique=True, nullable=False)
    parent_id = Column(Integer, ForeignKey("object_type.id", ondelete="cascade"), nullable=True)
    description_object_type = Column(String, nullable=True)

    children = relationship("ObjectTypeModel")
    object_drawing = relationship(
        "ObjectDrawingModel", back_populates="object_type", foreign_keys="ObjectDrawingModel.object_type_id"
    )
    object = relationship(
        "ObjectModel", back_populates="object_type", foreign_keys="ObjectModel.object_type_id"
    )

    def to_dc(self) -> ObjectTypeDC:
        return ObjectTypeDC(
            id=self.id,
            object_type_name=self.object_type_name,
            parent_id=self.parent_id,
            description_object_type=self.description_object_type,
            object_type_short_name=self.object_type_short_name,
        )

class ObjectDrawingModel(db):
    __tablename__ = "object_drawing"

    id = Column(Integer, primary_key=True, autoincrement=True)
    object_drawing_name = Column(String, unique=True, nullable=False)
    object_drawing_short_name = Column(String, unique=True, nullable=False)
    object_ref = Column(String, nullable=False)
    plan_ref = Column(String,nullable=False)
    drawing_scale = Column(Float, nullable=False)
    height = Column(Float, nullable=False)
    created_time = Column(DateTime, nullable=False)
    edited_time = Column(DateTime, nullable=False)
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    editor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    parent_id = Column(Integer, ForeignKey("object_drawing.id", ondelete="cascade"), nullable=True)
    object_type_id = Column(Integer, ForeignKey("object_type.id"), nullable=False)

    children = relationship("ObjectDrawingModel")
    usermade = relationship(
        "UserModel", back_populates="usermade", foreign_keys="ObjectDrawingModel.creator_id"
    )
    useredit = relationship(
        "UserModel", back_populates="useredit", foreign_keys="ObjectDrawingModel.editor_id"
    )
    object = relationship(
        "ObjectModel", back_populates="object_drawing", foreign_keys="ObjectModel.object_drawing_id"
    )
    object_type = relationship(
        "ObjectTypeModel", back_populates="object_drawing", foreign_keys="ObjectDrawingModel.object_type_id"
    )

    def to_dc(self) -> ObjectDrawingDC:
        return ObjectDrawingDC(
            id=self.id,
            object_drawing_name=self.object_drawing_name,
            parent_id=self.parent_id,
            object_drawing_short_name=self.object_drawing_short_name,
            object_ref=self.object_ref,
            plan_ref=self.plan_ref,
            drawing_scale=self.drawing_scale,
            height=self.height,
            created_time=self.created_time,
            edited_time=self.edited_time,
            creator_id=self.creator_id,
            editor_id=self.editor_id,
            object_type_id=self.object_type_id,
        )
class ObjectModel(db):
    __tablename__ = "object"

    id = Column(Integer, primary_key=True, autoincrement=True)
    object_name = Column(String, unique=True, nullable=False)
    object_short_name = Column(String, unique=True, nullable=False)
    svg_object = Column(JSON, nullable=False)
    parent_id = Column(Integer, ForeignKey("object.id", ondelete="cascade"), nullable=True)
    created_time = Column(DateTime, nullable=False)
    edited_time = Column(DateTime, nullable=False)
    object_type_id = Column(Integer, ForeignKey("object_type.id"), nullable=False)
    object_status_id = Column(Integer, ForeignKey("object_status.id"), nullable=False)
    object_drawing_id = Column(Integer, ForeignKey("object_drawing.id"), nullable=False)
    children = relationship("ObjectModel")
    object_drawing = relationship(
        "ObjectDrawingModel", back_populates="object", foreign_keys="ObjectModel.object_drawing_id"
    )
    object_type = relationship(
        "ObjectTypeModel", back_populates="object", foreign_keys="ObjectModel.object_type_id"
    )
    object_status = relationship(
        "ObjectStatusModel", back_populates="object", foreign_keys="ObjectModel.object_status_id"
    )
    route_point = relationship(
        "RoutePointModel", back_populates="object", foreign_keys="RoutePointModel.object_id"
    )

    def to_dc(self) -> ObjectDC:
        return ObjectDC(
            id=self.id,
            parent_id=self.parent_id,
            object_name=self.object_name,
            object_short_name=self.object_short_name,
            svg_object=self.svg_object,
            created_time=self.created_time,
            edited_time=self.edited_time,
            object_type_id=self.object_type_id,
            object_status_id=self.object_status_id,
            object_drawing_id=self.object_drawing_id,
        )
class RoutePointModel(db):
    __tablename__ = "route_point"

    id = Column(Integer, primary_key=True, autoincrement=True)
    route_point_name = Column(String, nullable=False)
    route_point_short_name = Column(String, nullable=False)
    svg_point = Column(JSON, nullable=False)
    created_time = Column(DateTime, nullable=False)
    edited_time = Column(DateTime, nullable=False)
    object_id = Column(Integer, ForeignKey("object.id"), nullable=False)
    point_type_id = Column(Integer, ForeignKey("point_type.id"), nullable=False)
    x_cord = Column(Float, nullable=False)
    y_cord = Column(Float, nullable=False)
    z_cord = Column(Float, nullable=False)

    point_type = relationship(
        "PointTypeModel", back_populates="route_point", foreign_keys="RoutePointModel.point_type_id"
    )
    object = relationship(
        "ObjectModel", back_populates="route_point", foreign_keys="RoutePointModel.object_id"
    )
    route_point1 = relationship(
        "PointConnectionModel", back_populates="route_point1", foreign_keys="PointConnectionModel.route_point1_id"
    )
    route_point2 = relationship(
        "PointConnectionModel", back_populates="route_point2", foreign_keys="PointConnectionModel.route_point2_id"
    )

    def to_dc(self) -> RoutePointDC:
        return RoutePointDC(
            id=self.id,
            route_point_name=self.route_point_name,
            route_point_short_name=self.route_point_short_name,
            svg_point=self.svg_point,
            created_time=self.created_time,
            edited_time=self.edited_time,
            object_id=self.object_id,
            point_type_id=self.point_type_id,
            x_cord=self.x_cord,
            y_cord=self.y_cord,
            z_cord=self.z_cord,
        )

class PointConnectionModel(db):
    __tablename__ = "point_connections"

    id = Column(Integer, primary_key=True, autoincrement=True)
    route_point1_id = Column(Integer, ForeignKey("route_point.id", ondelete="cascade"), nullable=False)
    route_point2_id = Column(Integer, ForeignKey("route_point.id", ondelete="cascade"), nullable=False)
    route_distance = Column(Float, nullable=False)
    route_time = Column(Float, nullable=False)
    weight_coefficient = Column(Float, nullable=False)
    direction_1_to_2 = Column(Integer, nullable=False)
    direction_2_to_1 = Column(Integer, nullable=False)

    __tableargs__ = (UniqueConstraint("route_point1_id", "route_point2_id", name="node_combination"),)

    route_point1 = relationship(
        "RoutePointModel", back_populates="route_point1", foreign_keys="PointConnectionModel.route_point1_id"
    )
    route_point2 = relationship(
        "RoutePointModel", back_populates="route_point2", foreign_keys="PointConnectionModel.route_point2_id"
    )

    def to_dc(self) -> PointConnectionDC:
        return PointConnectionDC(
            id=self.id,
            route_point1_id=self.route_point1_id,
            route_point2_id=self.route_point2_id,
            route_distance=self.route_distance,
            route_time=self.route_time,
            weight_coefficient=self.weight_coefficient,
            direction_1_to_2=self.direction_1_to_2,
            direction_2_to_1=self.direction_2_to_1,
        )
