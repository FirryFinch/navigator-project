import datetime
import json

import sqlalchemy.exc
from sqlalchemy import select, delete, update, or_

from app.base import BaseAccessor
from app.map.dataclasses import (
    RoutePointDC,
    ObjectTypeDC,
    ObjectDrawingDC,
    ObjectDC,
    ObjectStatusDC,
    PointTypeDC,
    PointConnectionDC,
    RoutePointsDC,
    ObjectTypesDC,
    ObjectDrawingsDC,
    ObjectsDC,
    PointTypesDC,
    ObjectStatusesDC,
    PointConnectionsDC
)

from app.map.models import RoutePointModel, ObjectTypeModel, ObjectDrawingModel, ObjectModel, PointTypeModel, ObjectStatusModel, PointConnectionModel


class MapAccessor(BaseAccessor):
    async def createObjectType(
        self, object_type_name: str, object_type_short_name: str, parent_id: int | None, description_object_type: str | None
    ) -> ObjectTypeDC | None:
        try:
            async with self.app.database.session() as session:
                ObjectType = ObjectTypeModel(
                    object_type_name=object_type_name,
                    object_type_short_name=object_type_short_name,
                    parent_id=parent_id,
                    description_object_type=description_object_type,
                )
                session.add(ObjectType)
                await session.commit()
                return ObjectType.to_dc()
        except sqlalchemy.exc.IntegrityError:
            return None
        except sqlalchemy.exc.ProgrammingError:
            return None

    async def createRoutePoint(
        self,
        route_point_name: str,
        route_point_short_name: str,
        svg_point: json,
        parent_id: int | None,
        object_id: int,
        point_type_id: int,
        x_cord: float,
        y_cord: float,
        z_cord: float,
    ) -> RoutePointDC | None:
        try:
            async with self.app.database.session() as session:
                RoutePoint = RoutePointModel(
                    route_point_name=route_point_name,
                    route_point_short_name=route_point_short_name,
                    svg_point=svg_point,
                    parent_id=parent_id,
                    object_id=object_id,
                    point_type_id=point_type_id,
                    x_cord=x_cord,
                    y_cord=y_cord,
                    z_cord=z_cord,
                    created_time=datetime.datetime.utcnow(),
                    edited_time=datetime.datetime.utcnow(),
                )
                session.add(RoutePoint)
                await session.commit()
                return RoutePoint.to_dc()
        except sqlalchemy.exc.IntegrityError:
            return None
        except sqlalchemy.exc.ProgrammingError:
            return None

    async def createObjectDrawing(
        self,
        object_drawing_name: str,
        object_drawing_short_name: str,
        object_ref: str,
        plan_ref: str,
        drawing_scale: float,
        height: float,
        user_id: int,
        object_type_id: int,
        parent_id: int | None,
    ) -> ObjectDrawingDC | None:
        try:
            async with self.app.database.session() as session:
                ObjectDrawing = ObjectDrawingModel(
                    object_drawing_name=object_drawing_name,
                    object_drawing_short_name=object_drawing_short_name,
                    parent_id=parent_id,
                    creator_id=user_id,
                    editor_id=user_id,
                    object_type_id=object_type_id,
                    object_ref=object_ref,
                    plan_ref=plan_ref,
                    drawing_scale=drawing_scale,
                    height=height,
                    created_time=datetime.datetime.utcnow(),
                    edited_time=datetime.datetime.utcnow(),
                )
                session.add(ObjectDrawing)
                await session.commit()
                return ObjectDrawing.to_dc()
        except sqlalchemy.exc.IntegrityError:
            return None
        except sqlalchemy.exc.ProgrammingError:
            return None

    async def createObject(
        self,
        object_name: str,
        object_short_name: str,
        svg_object: json,
        parent_id: int | None,
        object_status_id: int,
        object_drawing_id: int,
        object_type_id: int,
    ) -> ObjectDC | None:
        try:
            async with self.app.database.session() as session:
                Object = ObjectModel(
                    object_name=object_name,
                    object_short_name=object_short_name,
                    svg_object=svg_object,
                    parent_id=parent_id,
                    object_status_id=object_status_id,
                    object_drawing_id=object_drawing_id,
                    object_type_id=object_type_id,
                    created_time=datetime.datetime.utcnow(),
                    edited_time=datetime.datetime.utcnow(),
                )
                session.add(Object)
                await session.commit()
                return Object.to_dc()
        except sqlalchemy.exc.IntegrityError:
            return None
        except sqlalchemy.exc.ProgrammingError:
            return None

    async def createPointType(
        self,
        point_name: str,
        point_short_name: str,
        description: str,
    ) -> PointTypeDC | None:
        try:
            async with self.app.database.session() as session:
                PointType = PointTypeModel(
                    point_name=point_name,
                    point_short_name=point_short_name,
                    description=description,
                )
                session.add(PointType)
                await session.commit()
                return PointType.to_dc()
        except sqlalchemy.exc.IntegrityError:
            return None
        except sqlalchemy.exc.ProgrammingError:
            return None

    async def createObjectStatus(
        self,
        object_status_name: str,
    ) -> ObjectStatusDC | None:
        try:
            async with self.app.database.session() as session:
                ObjectStatus = ObjectStatusModel(
                    object_status_name=object_status_name,
                )
                session.add(ObjectStatus)
                await session.commit()
                return ObjectStatus.to_dc()
        except sqlalchemy.exc.IntegrityError:
            return None
        except sqlalchemy.exc.ProgrammingError:
            return None

    async def createPointConnection(
        self, route_point1_id: int, route_point2_id: int, route_distance: float, route_time: float, weight_coefficient: float, direction_1_to_2: int,  direction_2_to_1: int
    ) -> PointConnectionDC | None:
        try:
            async with self.app.database.session() as session:
                connection = PointConnectionModel(
                    route_point1_id=route_point1_id,
                    route_point2_id=route_point2_id,
                    route_distance=route_distance,
                    route_time=route_time,
                    weight_coefficient=weight_coefficient,
                    direction_1_to_2=direction_1_to_2,
                    direction_2_to_1=direction_2_to_1,
                )
                session.add(connection)
                await session.commit()
                return connection.to_dc()
        except sqlalchemy.exc.IntegrityError:
            return None
        except sqlalchemy.exc.ProgrammingError:
            return None

    async def deleteObject(self, id: int) -> False | True:
        try:
            async with self.app.database.session() as session:
                query = delete(ObjectModel).where(ObjectModel.id == id)
                await session.execute(query)
                await session.commit()
                return True
        except sqlalchemy.exc.IntegrityError:
            return False
        except sqlalchemy.exc.ProgrammingError:
            return False

    async def deleteRoutePoint(self, id: int) -> False | True:
        try:
            async with self.app.database.session() as session:
                query = delete(RoutePointModel).where(RoutePointModel.id == id)
                await session.execute(query)
                await session.commit()
                return True
        except sqlalchemy.exc.IntegrityError:
            return False
        except sqlalchemy.exc.ProgrammingError:
            return False

    async def deleteObjectDrawing(self, id: int) -> False | True:
        try:
            async with self.app.database.session() as session:
                query = delete(ObjectDrawingModel).where(ObjectDrawingModel.id == id)
                await session.execute(query)
                await session.commit()
                return True
        except sqlalchemy.exc.IntegrityError:
            return False
        except sqlalchemy.exc.ProgrammingError:
            return False

    async def deleteObjectType(self, id: int) -> False | True:
        try:
            async with self.app.database.session() as session:
                query = delete(ObjectTypeModel).where(ObjectTypeModel.id == id)
                await session.execute(query)
                await session.commit()
                return True
        except sqlalchemy.exc.IntegrityError:
            return False
        except sqlalchemy.exc.ProgrammingError:
            return False

    async def deleteObjectStatus(self, id: int) -> False | True:
        try:
            async with self.app.database.session() as session:
                query = delete(ObjectStatusModel).where(ObjectStatusModel.id == id)
                await session.execute(query)
                await session.commit()
                return True
        except sqlalchemy.exc.IntegrityError:
            return False
        except sqlalchemy.exc.ProgrammingError:
            return False

    async def deletePointType(self, id: int) -> False | True:
        try:
            async with self.app.database.session() as session:
                query = delete(PointTypeModel).where(PointTypeModel.id == id)
                await session.execute(query)
                await session.commit()
                return True
        except sqlalchemy.exc.IntegrityError:
            return False
        except sqlalchemy.exc.ProgrammingError:
            return False

    async def deletePointConnection(self, id: int) -> False | True:
        try:
            async with self.app.database.session() as session:
                query = delete(PointConnectionModel).where(PointConnectionModel.id == id)
                await session.execute(query)
                await session.commit()
                return True
        except sqlalchemy.exc.IntegrityError:
            return False
        except sqlalchemy.exc.ProgrammingError:
            return False

    async def get_object_by_id(self, id: int) -> ObjectDC | None:
        async with self.app.database.session() as session:
            query = select(ObjectModel).where(ObjectModel.id == id)
            res = await session.scalars(query)
            object = res.one_or_none()
            if object:
                return ObjectDC(
                    id=object.id,
                    object_name=object.object_name,
                    object_short_name=object.object_short_name,
                    svg_object=object.svg_object,
                    parent_id=object.parent_id,
                    object_status_id=object.object_status_id,
                    object_drawing_id=object.object_drawing_id,
                    object_type_id=object.object_type_id,
                    created_time=object.created_time,
                    edited_time=object.edited_time,
                )
            return None

    async def get_route_point_by_id(self, id: int) -> RoutePointDC | None:
        async with self.app.database.session() as session:
            query = select(RoutePointModel).where(RoutePointModel.id == id)
            res = await session.scalars(query)
            route_point = res.one_or_none()
            if route_point:
                return RoutePointDC(
                    id=route_point.id,
                    route_point_name=route_point.route_point_name,
                    route_point_short_name=route_point.route_point_short_name,
                    svg_point=route_point.svg_point,
                    object_id=route_point.object_id,
                    point_type_id=route_point.point_type_id,
                    x_cord=route_point.x_cord,
                    y_cord=route_point.y_cord,
                    z_cord=route_point.z_cord,
                    created_time=route_point.created_time,
                    edited_time=route_point.edited_time,
                )
            return None

    async def get_object_type_by_id(self, id: int) -> ObjectTypeDC | None:
        async with self.app.database.session() as session:
            query = select(ObjectTypeModel).where(ObjectTypeModel.id == id)
            res = await session.scalars(query)
            object_type = res.one_or_none()
            if object_type:
                return ObjectTypeDC(
                    id=object_type.id,
                    object_type_name=object_type.object_type_name,
                    object_type_short_name=object_type.object_type_short_name,
                    parent_id=object_type.parent_id,
                    description_object_type=object_type.description_object_type,
                )
            return None

    async def get_object_drawing_by_id(self, id: int) -> ObjectDrawingDC | None:
        async with self.app.database.session() as session:
            query = select(ObjectDrawingModel).where(ObjectDrawingModel.id == id)
            res = await session.scalars(query)
            object_drawing = res.one_or_none()
            if object_drawing:
                return ObjectDrawingDC(
                    id=object_drawing.id,
                    object_drawing_name=object_drawing.object_drawing_name,
                    object_drawing_short_name=object_drawing.object_drawing_short_name,
                    parent_id=object_drawing.parent_id,
                    creator_id=object_drawing.creator_id,
                    editor_id=object_drawing.editor_id,
                    object_type_id=object_drawing.object_type_id,
                    object_ref=object_drawing.object_ref,
                    plan_ref=object_drawing.plan_ref,
                    drawing_scale=object_drawing.drawing_scale,
                    height=object_drawing.height,
                    created_time=object_drawing.created_time,
                    edited_time=object_drawing.edited_time,
                )
            return None

    async def get_point_type_by_id(self, id: int) -> PointTypeDC | None:
        async with self.app.database.session() as session:
            query = select(PointTypeModel).where(PointTypeModel.id == id)
            res = await session.scalars(query)
            point_type = res.one_or_none()
            if point_type:
                return PointTypeDC(
                    id=point_type.id,
                    point_name=point_type.point_name,
                    point_short_name=point_type.point_short_name,
                    description=point_type.description,
                )
            return None

    async def get_point_connection_by_id(self, id: int) -> PointConnectionDC | None:
        async with self.app.database.session() as session:
            query = select(PointConnectionModel).where(PointConnectionModel.id == id)
            res = await session.scalars(query)
            point_connection = res.one_or_none()
            if point_connection:
                return PointConnectionDC(
                    id=point_connection.id,
                    route_point1_id=point_connection.route_point1_id,
                    route_point2_id=point_connection.route_point2_id,
                    route_distance=point_connection.route_distance,
                    route_time=point_connection.route_time,
                    weight_coefficient=point_connection.weight_coefficient,
                    direction_1_to_2=point_connection.direction_1_to_2,
                    direction_2_to_1=point_connection.direction_2_to_1,
                )
            return None

    async def get_object_status_by_id(self, id: int) -> ObjectStatusDC | None:
        async with self.app.database.session() as session:
            query = select(ObjectStatusModel).where(ObjectStatusModel.id == id)
            res = await session.scalars(query)
            object_status = res.one_or_none()
            if object_status:
                return ObjectStatusDC(
                    id=object_status.id,
                    object_status_name=object_status.object_status_name,
                )
            return None
    async def update_RoutePointinfo(
            self,
            id: int,
            route_point_name: str,
            route_point_short_name: str,
            svg_point: json,
            parent_id: int | None,
            object_id: int,
            point_type_id: int,
            x_cord: float,
            y_cord: float,
            z_cord: float,
    ) -> RoutePointDC | None:
        try:
            async with self.app.database.session() as session:
                query = (
                    update(RoutePointModel)
                    .where(RoutePointModel.id == id)
                    .values(
                        route_point_name=route_point_name,
                        route_point_short_name=route_point_short_name,
                        svg_point=svg_point,
                        parent_id=parent_id,
                        object_id=object_id,
                        point_type_id=point_type_id,
                        x_cord=x_cord,
                        y_cord=y_cord,
                        z_cord=z_cord,
                        created_time=datetime.datetime.utcnow(),
                        edited_time=datetime.datetime.utcnow(),
                    )
                )
                await session.execute(query)
                await session.commit()
                route_point = await self.get_route_point_by_id(id)
                return route_point
        except sqlalchemy.exc.IntegrityError:
            return None
        except sqlalchemy.exc.ProgrammingError:
            return None

    async def update_ObjectTypeinfo(
        self, id: int, object_type_name: str, object_type_short_name: str, parent_id: int | None, description_object_type: str | None
    ) -> ObjectTypeDC | None:
        try:
            async with self.app.database.session() as session:
                query = (
                    update(ObjectTypeModel)
                    .where(ObjectTypeModel.id == id)
                    .values(
                        object_type_name=object_type_name,
                        object_type_short_name=object_type_short_name,
                        parent_id=parent_id,
                        description=description_object_type,
                    )
                )
                await session.execute(query)
                await session.commit()
                object_type = await self.get_object_type_by_id(id)
                return object_type
        except sqlalchemy.exc.IntegrityError:
            return None
        except sqlalchemy.exc.ProgrammingError:
            return None

    async def update_PointConninfo(
        self, id: int, route_point1_id: int, route_point2_id: int, route_distance: float, route_time: float, weight_coefficient: float, direction_1_to_2: int,  direction_2_to_1: int
    ) -> PointConnectionDC | None:
        try:
            async with self.app.database.session() as session:
                query = (
                    update(PointConnectionModel)
                    .where(PointConnectionModel.id == id)
                    .values(
                        route_point1_id=route_point1_id,
                        route_point2_id=route_point2_id,
                        route_distance=route_distance,
                        route_time=route_time,
                        weight_coefficient=weight_coefficient,
                        direction_1_to_2=direction_1_to_2,
                        direction_2_to_1=direction_2_to_1,
                    )
                )
                await session.execute(query)
                await session.commit()
                point_connection = await self.get_point_connection_by_id(id)
                return point_connection
        except sqlalchemy.exc.IntegrityError:
            return None
        except sqlalchemy.exc.ProgrammingError:
            return None

    async def update_ObjectDrawinginfo(
            self,
            id: int,
            object_drawing_name: str,
            object_drawing_short_name: str,
            object_ref: str,
            plan_ref: str,
            drawing_scale: float,
            height: float,
            user_id: int,
            object_type_id: int,
            parent_id: int | None,
    ) -> ObjectDrawingDC | None:
        try:
            async with self.app.database.session() as session:
                query = (
                    update(ObjectDrawingModel)
                    .where(ObjectDrawingModel.id == id)
                    .values(
                        object_drawing_name=object_drawing_name,
                        object_drawing_short_name=object_drawing_short_name,
                        parent_id=parent_id,
                        creator_id=user_id,
                        editor_id=user_id,
                        object_type_id=object_type_id,
                        object_ref=object_ref,
                        plan_ref=plan_ref,
                        drawing_scale=drawing_scale,
                        height=height,
                        created_time=datetime.datetime.utcnow(),
                        edited_time=datetime.datetime.utcnow(),
                    )
                )
                await session.execute(query)
                await session.commit()
                object_drawing = await self.get_object_drawing_by_id(id)
                return object_drawing
        except sqlalchemy.exc.IntegrityError:
            return None
        except sqlalchemy.exc.ProgrammingError:
            return None

    async def update_Objectinfo(
            self,
            id: int,
            object_name: str,
            object_short_name: str,
            svg_object: json,
            parent_id: int | None,
            object_status_id: int,
            object_drawing_id: int,
            object_type_id: int,
    ) -> ObjectDC | None:
        try:
            async with self.app.database.session() as session:
                query = (
                    update(ObjectModel)
                    .where(ObjectModel.id == id)
                    .values(
                        object_name=object_name,
                        object_short_name=object_short_name,
                        svg_object=svg_object,
                        parent_id=parent_id,
                        object_status_id=object_status_id,
                        object_drawing_id=object_drawing_id,
                        object_type_id=object_type_id,
                        created_time=datetime.datetime.utcnow(),
                        edited_time=datetime.datetime.utcnow(),
                    )
                )
                await session.execute(query)
                await session.commit()
                object = await self.get_object_by_id(id)
                return object
        except sqlalchemy.exc.IntegrityError:
            return None
        except sqlalchemy.exc.ProgrammingError:
            return None

    async def update_ObjectStatusinfo(
            self,
            id: int,
            object_status_name: str,
    ) -> ObjectStatusDC | None:
        try:
            async with self.app.database.session() as session:
                query = (
                    update(ObjectStatusModel)
                    .where(ObjectStatusModel.id == id)
                    .values(
                        object_status_name=object_status_name,
                    )
                )
                await session.execute(query)
                await session.commit()
                object_status = await self.get_object_status_by_id(id)
                return object_status
        except sqlalchemy.exc.IntegrityError:
            return None
        except sqlalchemy.exc.ProgrammingError:
            return None

    async def update_PointTypeinfo(
            self,
            id: int,
            point_name: str,
            point_short_name: str,
            description: str,
    ) -> PointTypeDC | None:
        try:
            async with self.app.database.session() as session:
                query = (
                    update(PointTypeModel)
                    .where(PointTypeModel.id == id)
                    .values(
                        point_name=point_name,
                        point_short_name=point_short_name,
                        description=description,
                    )
                )
                await session.execute(query)
                await session.commit()
                point_type = await self.get_point_type_by_id(id)
                return point_type
        except sqlalchemy.exc.IntegrityError:
            return None
        except sqlalchemy.exc.ProgrammingError:
            return None

    async def get_all_route_point(self, page: int | None, limit: int | None) -> RoutePointsDC | None:
        try:
            async with self.app.database.session() as session:
                if page and limit:
                    query = select(RoutePointModel).limit(limit).offset((page - 1) * limit).order_by(RoutePointModel.id)
                else:
                    query = select(RoutePointModel).order_by(RoutePointModel.id)
                res = await session.scalars(query)
                results = res.all()
                if results:
                    return RoutePointsDC(
                        routes_points=[
                            RoutePointDC(
                                id=route_point.id,
                                route_point_name=route_point.route_point_name,
                                route_point_short_name=route_point.route_point_short_name,
                                svg_point=route_point.svg_point,
                                object_id=route_point.object_id,
                                point_type_id=route_point.point_type_id,
                                x_cord=route_point.x_cord,
                                y_cord=route_point.y_cord,
                                z_cord=route_point.z_cord,
                                created_time=route_point.created_time,
                                edited_time=route_point.edited_time,
                            )
                            for route_point in results
                        ]
                    )
                else:
                    return None
        except sqlalchemy.exc.IntegrityError:
            return None

    async def get_all_objects(self, page: int | None, limit: int | None) -> ObjectsDC | None:
        try:
            async with self.app.database.session() as session:
                if page and limit:
                    query = select(ObjectModel).limit(limit).offset((page - 1) * limit).order_by(ObjectModel.id)
                else:
                    query = select(ObjectModel).order_by(ObjectModel.id)
                res = await session.scalars(query)
                results = res.all()
                if results:
                    return ObjectsDC(
                        objects=[
                            ObjectDC(
                                id=object.id,
                                object_name=object.object_name,
                                object_short_name=object.object_short_name,
                                svg_object=object.svg_object,
                                parent_id=object.parent_id,
                                object_status_id=object.object_status_id,
                                object_drawing_id=object.object_drawing_id,
                                object_type_id=object.object_type_id,
                                created_time=object.created_time,
                                edited_time=object.edited_time,
                            )
                            for object in results
                        ]
                    )
                else:
                    return None
        except sqlalchemy.exc.IntegrityError:
            return None

    async def get_all_object_types(
        self, page: int | None, limit: int | None
    ) -> ObjectTypesDC | None:
        try:
            async with self.app.database.session() as session:
                if page and limit:
                    query = (
                        select(ObjectTypeModel)
                        .limit(limit)
                        .offset((page - 1) * limit).order_by(ObjectTypeModel.id)
                    )
                else:
                    query = select(ObjectTypeModel).order_by(ObjectTypeModel.id)
                res = await session.scalars(query)
                results = res.all()
                if results:
                    return ObjectTypesDC(
                        objects_types=[
                            ObjectTypeDC(
                                id=object_type.id,
                                object_type_name=object_type.object_type_name,
                                object_type_short_name=object_type.object_type_short_name,
                                parent_id=object_type.parent_id,
                                description_object_type=object_type.description_object_type,
                            )
                            for object_type in results
                        ]
                    )
                else:
                    return None
        except sqlalchemy.exc.IntegrityError:
            return None

    async def get_all_object_drawings(
        self, page: int | None, limit: int | None
    ) -> ObjectDrawingsDC | None:
        try:
            async with self.app.database.session() as session:
                if page and limit:
                    query = (
                        select(ObjectDrawingModel)
                        .limit(limit)
                        .offset((page - 1) * limit).order_by(ObjectDrawingModel.id)
                    )
                else:
                    query = select(ObjectDrawingModel).order_by(ObjectDrawingModel.id)
                res = await session.scalars(query)
                results = res.all()
                if results:
                    return ObjectDrawingsDC(
                        objects_drawings=[
                            ObjectDrawingDC(
                                id=object_drawing.id,
                                object_drawing_name=object_drawing.object_drawing_name,
                                object_drawing_short_name=object_drawing.object_drawing_short_name,
                                parent_id=object_drawing.parent_id,
                                creator_id=object_drawing.creator_id,
                                editor_id=object_drawing.editor_id,
                                object_type_id=object_drawing.object_type_id,
                                object_ref=object_drawing.object_ref,
                                plan_ref=object_drawing.plan_ref,
                                drawing_scale=object_drawing.drawing_scale,
                                height=object_drawing.height,
                                created_time=object_drawing.created_time,
                                edited_time=object_drawing.edited_time,
                            )
                            for object_drawing in results
                        ]
                    )
                else:
                    return None
        except sqlalchemy.exc.IntegrityError:
            return None

    async def get_all_point_types(
        self, page: int | None, limit: int | None
    ) -> PointTypesDC | None:
        try:
            async with self.app.database.session() as session:
                if page and limit:
                    query = (
                        select(PointTypeModel)
                        .limit(limit)
                        .offset((page - 1) * limit).order_by(PointTypeModel.id)
                    )
                else:
                    query = select(PointTypeModel).order_by(PointTypeModel.id)
                res = await session.scalars(query)
                results = res.all()
                if results:
                    return PointTypesDC(
                        points_types=[
                            PointTypeDC(
                                id=point_type.id,
                                point_name=point_type.point_name,
                                point_short_name=point_type.point_short_name,
                                description=point_type.description,
                            )
                            for point_type in results
                        ]
                    )
                else:
                    return None
        except sqlalchemy.exc.IntegrityError:
            return None

    async def get_all_point_connections(
        self, page: int | None, limit: int | None
    ) -> PointConnectionsDC | None:
        try:
            async with self.app.database.session() as session:
                if page and limit:
                    query = (
                        select(PointConnectionModel)
                        .limit(limit)
                        .offset((page - 1) * limit).order_by(PointConnectionModel.id)
                    )
                else:
                    query = select(PointConnectionModel).order_by(PointConnectionModel.id)
                res = await session.scalars(query)
                results = res.all()
                if results:
                    return PointConnectionsDC(
                        points_conns=[
                            PointConnectionDC(
                                id=point_connection.id,
                                route_point1_id=point_connection.route_point1_id,
                                route_point2_id=point_connection.route_point2_id,
                                route_distance=point_connection.route_distance,
                                route_time=point_connection.route_time,
                                weight_coefficient=point_connection.weight_coefficient,
                                direction_1_to_2=point_connection.direction_1_to_2,
                                direction_2_to_1=point_connection.direction_2_to_1,
                            )
                            for point_connection in results
                        ]
                    )
                else:
                    return None
        except sqlalchemy.exc.IntegrityError:
            return None
    async def get_all_point_connections_of_node(self, route_point_id: int) -> PointConnectionsDC | None:
        try:
            async with self.app.database.session() as session:
                query = select(PointConnectionModel).where(
                    or_(
                        PointConnectionModel.route_point1_id == route_point_id,
                        PointConnectionModel.route_point2_id == route_point_id,
                    )
                ).order_by(PointConnectionModel.id)
                res = await session.scalars(query)
                results = res.all()
                if results:
                    return PointConnectionsDC(
                        points_conns=[
                            PointConnectionDC(
                                id=point_connection.id,
                                route_point1_id=point_connection.route_point1_id,
                                route_point2_id=point_connection.route_point2_id,
                                route_distance=point_connection.route_distance,
                                route_time=point_connection.route_time,
                                weight_coefficient=point_connection.weight_coefficient,
                                direction_1_to_2=point_connection.direction_1_to_2,
                                direction_2_to_1=point_connection.direction_2_to_1,
                            )
                            for point_connection in results
                        ]
                    )
                else:
                    return None
        except sqlalchemy.exc.IntegrityError:
            return None

    async def get_all_object_status(
            self, page: int | None, limit: int | None
    ) -> ObjectStatusesDC | None:
        try:
            async with self.app.database.session() as session:
                if page and limit:
                    query = (
                        select(ObjectStatusModel)
                        .limit(limit)
                        .offset((page - 1) * limit).order_by(ObjectStatusModel.id)
                    )
                else:
                    query = select(ObjectStatusModel).order_by(ObjectStatusModel.id)
                res = await session.scalars(query)
                results = res.all()
                if results:
                    return ObjectStatusesDC(
                        objects_status=[
                            ObjectStatusDC(
                                id=object_status.id,
                                object_status_name=object_status.object_status_name,
                            )
                            for object_status in results
                        ]
                    )
                else:
                    return None
        except sqlalchemy.exc.IntegrityError:
            return None

    async def get_all_children_object_types(self, object_type_id: int) -> ObjectTypesDC | None:
        try:
            async with self.app.database.session() as session:
                query = select(ObjectTypeModel).where(ObjectTypeModel.parent_id == object_type_id).order_by(ObjectTypeModel.id)
                res = await session.scalars(query)
                results = res.all()
                if results:
                    return ObjectTypesDC(
                        objects_types=[
                            ObjectTypeDC(
                                id=object_type.id,
                                object_type_name=object_type.object_type_name,
                                object_type_short_name=object_type.object_type_short_name,
                                parent_id=object_type.parent_id,
                                description=object_type.description_object_type,
                            )
                            for object_type in results
                        ]
                    )
                else:
                    return None
        except sqlalchemy.exc.IntegrityError:
            return None

    async def get_all_children_of_object(self, object_id: int) -> ObjectsDC | None:
        try:
            async with self.app.database.session() as session:
                query = select(ObjectModel).where(ObjectModel.type_id == object_id).order_by(ObjectModel.id)
                res = await session.scalars(query)
                results = res.all()
                if results:
                    return ObjectsDC(
                        objects=[
                            ObjectDC(
                                id=object.id,
                                object_name=object.object_name,
                                object_short_name=object.object_short_name,
                                svg_object=object.svg_object,
                                parent_id=object.parent_id,
                                object_status_id=object.object_status_id,
                                object_drawing_id=object.object_drawing_id,
                                object_type_id=object.object_type_id,
                                created_time=object.created_time,
                                edited_time=object.edited_time,
                            )
                            for object in results
                        ]
                    )
                else:
                    return None
        except sqlalchemy.exc.IntegrityError:
            return None

    async def get_all_children_of_object_drawings(self, object_drawing_id: int) -> ObjectDrawingsDC | None:
        try:
            async with self.app.database.session() as session:
                query = select(ObjectDrawingModel).where(ObjectDrawingModel.type_id == object_drawing_id).order_by(ObjectDrawingModel.id)
                res = await session.scalars(query)
                results = res.all()
                if results:
                    return ObjectDrawingsDC(
                        objects_drawings=[
                            ObjectDrawingDC(
                                id=object_drawing.id,
                                object_drawing_name=object_drawing.object_drawing_name,
                                object_drawing_short_name=object_drawing.object_drawing_short_name,
                                parent_id=object_drawing.parent_id,
                                creator_id=object_drawing.creator_id,
                                editor_id=object_drawing.editor_id,
                                object_type_id=object_drawing.object_type_id,
                                object_ref=object_drawing.object_ref,
                                plan_ref=object_drawing.plan_ref,
                                drawing_scale=object_drawing.drawing_scale,
                                height=object_drawing.height,
                                created_time=object_drawing.created_time,
                                edited_time=object_drawing.edited_time,
                            )
                            for object_drawing in results
                        ]
                    )
                else:
                    return None
        except sqlalchemy.exc.IntegrityError:
            return None
