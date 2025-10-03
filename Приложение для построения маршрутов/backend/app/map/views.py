from aiohttp.web_exceptions import (
    HTTPForbidden,
    HTTPUnauthorized,
    HTTPBadRequest,
    HTTPNotFound,
    HTTPServiceUnavailable
)
from aiohttp_apispec import (
    request_schema,
)

from aiohttp_cors import CorsViewMixin
from app.web.app import View
from app.web.utils import json_response

from app.map.schemas import (
    NewObjectSchema,
    NewPointTypeSchema,
    UpdPointTypeSchema,
    UpdObjectSchema,
    NewObjectStatusSchema,
    UpdObjectStatusSchema,
    NewPointConnSchema,
    UpdPointConnSchema,
    NewRoutePointSchema,
    UpdRoutePointSchema,
    NewObjectTypeSchema,
    UpdObjecTypeSchema,
    NewObjectDrawingsSchema,
    UpdObjectDrawingsSchema
)
from app.user.dataclasses import KEY_TYPES


class NavigateView(CorsViewMixin, View):
    async def get(self):
        if not self.store.map.working:
            raise HTTPServiceUnavailable(reason="Модуль навигации еще не запущен. Запустите навигатор и попробуйте снова.")
        try:
            start_id = int(self.request.query.get("start_id"))
            target_id = int(self.request.query.get("target_id"))
        except:
            raise HTTPBadRequest(resaon="Не указаны необходимые параметры") 
        if not start_id or not target_id:
            raise HTTPBadRequest(resaon="Не указаны необходимые параметры")
        start_node = await self.store.mapAPI.get_route_point_by_id(start_id)
        target_node = await self.store.mapAPI.get_route_point_by_id(target_id)
        if (start_node is None) or (target_node is None):
            raise HTTPNotFound(resaon="Не существует указанной зоны")
        route = await self.store.map.navigate_main(start_id, target_id)
        return json_response(
            data={
                "route": [
                    {"id": route_node.id, "name": route_node.route_point_name} for route_node in route
                ]
            }
        )


class StartView(CorsViewMixin, View):
    async def post(self):
        if not self.store.map.working:
            await self.store.map.start()
            return json_response(data={"result": "Система навигации запущена успешно"})
        else:
            return json_response(data={"result": "Система навигации уже запущена"})


class ObjectView(CorsViewMixin, View):
    async def get(self):
        try:
            object_id = int(self.request.rel_url.name)
        except:
            page = int(self.request.query.get("page", 1))
            if page < 1:
                raise HTTPBadRequest(resaon="Неверный параметр")
            unlimited = int(self.request.query.get("unlimited", 0))
            if unlimited == 1:
                objects = await self.store.mapAPI.get_all_objects(page=None,limit=None)
            else:
                objects = await self.store.mapAPI.get_all_objects(page=page, limit=10)
            if not objects:
                raise HTTPNotFound(resaon="Вы вышли за границы списка")
            return json_response(
                data=[
                    {
                        "id": object.id,
                        "parent_id": object.parent_id,
                        "object_name": object.object_name,
                        "object_short_name": object.object_short_name,
                        "svg_object": object.svg_object,
                        "object_status_id": object.object_status_id,
                        "object_drawing_id": object.object_drawing_id,
                        "object_type_id":object.object_type_id,
                    }
                    for object in objects.objects
                ]
            )
        search_object = await self.store.mapAPI.get_object_by_id(object_id)
        if search_object is None:
            raise HTTPNotFound(resaon="Не существует")
        return json_response(
            data={
                "id": search_object.id,
                "parent_id": search_object.parent_id,
                "object_name": search_object.object_name,
                "object_short_name": search_object.object_short_name,
                "svg_object": search_object.svg_object,
                "object_status_id": search_object.object_status_id,
                "object_drawing_id": search_object.object_drawing_id,
                "object_type_id":search_object.object_type_id,
            }
        )

    @request_schema(NewObjectSchema)
    async def post(self):
        if self.request.user is None:
            raise HTTPUnauthorized(resaon="Нет авторизации")
        user = self.request.user
        acceses = await self.store.userAPI.get_user_accesses(user.id)
        if acceses is None:
            raise HTTPForbidden(resaon="Доступ к ресурсу запрещен")
        roles = [access.access_id.category_name for access in acceses.roles]
        if (KEY_TYPES.ADMIN not in roles) and (KEY_TYPES.OWNER not in roles):
            raise HTTPForbidden(resaon="Доступ к ресурсу запрещен")
        new_object = await self.store.mapAPI.createObject(
            object_name=self.data["object_name"],
            object_short_name=self.data["object_short_name"],
            parent_id=self.data.get("parent_id"),
            svg_object=self.data.get("svg_object"),
            description=self.data.get("description"),
            object_status_id=self.data.get("object_status_id"),
            object_drawing_id=self.data.get("object_drawing_id"),
            object_type_id=self.data.get("object_type_id"),
        )
        if new_object is None:
            raise HTTPBadRequest(resaon="Ошибка при создании")
        return json_response(
            data={
                "id": new_object.id,
                "parent_id": new_object.parent_id,
                "object_name": new_object.object_name,
                "object_short_name": new_object.object_short_name,
                "svg_object": new_object.svg_object,
                "object_status_id": new_object.object_status_id,
                "object_drawing_id": new_object.object_drawing_id,
                "object_type_id": new_object.object_type_id,
            }
        )

    @request_schema(UpdObjectSchema)
    async def put(self):
        if self.request.user is None:
            raise HTTPUnauthorized(resaon="Вы не авторизованы")
        user = self.request.user
        acceses = await self.store.userAPI.get_user_accesses(user.id)
        if acceses is None:
            raise HTTPForbidden(resaon="Доступ к ресурсу запрещен")
        roles = [access.access_id.category_name for access in acceses.roles]
        if (KEY_TYPES.ADMIN not in roles) and (KEY_TYPES.OWNER not in roles):
            raise HTTPForbidden(resaon="Доступ к ресурсу запрещен")
        try:
            object_id = int(self.request.rel_url.name)
        except:
            raise HTTPBadRequest(resaon="Не указан тип")
        search_object = await self.store.mapAPI.get_object_by_id(object_id)
        if search_object is None:
            raise HTTPNotFound(resaon="Нет такого объекта")
        if self.data.get("object_name"):
            search_object.name = self.data.get("object_name")
        if self.data.get("object_short_name"):
            search_object.shortname = self.data.get("object_short_name")
        upd_object = await self.store.mapAPI.update_Objectinfo(
            id=object_id,
            object_name=search_object.object_name,
            object_short_name=search_object.object_short_name,
            svg_object=search_object.svg_object,
        )
        if upd_object is None:
            raise HTTPBadRequest("Ошибка при изменении")
        return json_response(
            data={
                "id": upd_object.id,
                "parent_id": upd_object.parent_id,
                "object_name": upd_object.object_name,
                "object_short_name": upd_object.object_short_name,
                "svg_object": upd_object.svg_object,
                "object_status_id": upd_object.object_status_id,
                "object_drawing_id": upd_object.object_drawing_id,
                "object_type_id": upd_object.object_type_id,
            }
        )

    async def delete(self):
        if self.request.user is None:
            raise HTTPUnauthorized(resaon="Вы не авторизованы")
        user = self.request.user
        acceses = await self.store.userAPI.get_user_accesses(user.id)
        if acceses is None:
            raise HTTPForbidden(resaon="Доступ к ресурсу запрещен")
        roles = [access.access_id.category_name for access in acceses.roles]
        if (KEY_TYPES.ADMIN not in roles) and (KEY_TYPES.OWNER not in roles):
            raise HTTPForbidden(resaon="Доступ к ресурсу запрещен")
        try:
            object_id = int(self.request.rel_url.name)
        except:
            raise HTTPBadRequest(resaon="Нет указан ресурс")
        search_object = await self.store.mapAPI.get_object_by_id(object_id)
        if search_object is None:
            raise HTTPNotFound(resaon="Указанный ресурс не существует")
        result = await self.store.mapAPI.deleteObject(object_id)
        if not result:
            raise HTTPBadRequest(resaon="Ошибка при удалении")
        return json_response(data={"result": "Успешное удаление"})


class RoutePointView(CorsViewMixin, View):
    async def get(self):
        try:
            route_point_id = int(self.request.rel_url.name)
        except:
            page = int(self.request.query.get("page", 1))
            if page < 1:
                raise HTTPBadRequest(resaon="Неправильный параметр")
            route_point_type = int(self.request.query.get("type", 0))
            if route_point_type < 0:
                raise HTTPBadRequest(resaon="Неправильный параметр")
            unlimited = int(self.request.query.get("unlimited", 0))
            parent = int(self.request.query.get("parent_node", 0))
            if parent < 0:
                raise HTTPBadRequest(resaon="Неправильный параметр")
            if unlimited == 1:
                route_points = await self.store.mapAPI.get_all_route_point(page=None,limit=None)
           # elif route_point_type:
           #     route_points = await self.store.mapAPI.get_all_children_of_type(route_point_type)
           # elif parent:
            #    route_points = await self.store.mapAPI.get_all_children_nodes_of_node(parent)
            else:
                route_points = await self.store.mapAPI.get_all_route_point(page=page, limit=10)
            if not route_points:
                raise HTTPNotFound(resaon="Вы вышли за пределы списка зон")
            try:
                user = self.request.user
                acceses = await self.store.userAPI.get_user_accesses(user.id)
                roles = [access.access_id.category_name for access in acceses.roles]
                if (
                    (KEY_TYPES.ADMIN in roles)
                    or (KEY_TYPES.OWNER in roles)
                    or (KEY_TYPES.EDITOR in roles)
                ):
                    return json_response(
                        data={
                            "route_points": [
                                {
                                    "id": route_points.id,
                                    "parent_id": route_points.parent_id,
                                    "created_time": route_points.created_time.strftime(
                                        "%Y-%m-%dT%H:%M:%S.%fZ"
                                    ),
                                    "edited_time": route_points.edited_time.strftime(
                                        "%Y-%m-%dT%H:%M:%S.%fZ"
                                    ),
                                    "type": route_points.type_id,
                                    "route_point_name": route_points.route_point_name,
                                    "route_point_short_name": route_points.route_point_short_name,
                                    "svg_point": route_points.svg_point,
                                    "x_cord": route_points.x_cord,
                                    "y_cord": route_points.y_cord,
                                    "z_cord": route_points.z_cord,
                                    "point_type_id": route_points.point_type_id,
                                    "object_id": route_points.object_id,
                                }
                                for route_points in route_points.routes_points
                            ]
                        }
                    )
            except:
                return json_response(
                data={
                    "nodes": [
                        {
                            "id": route_points.id,
                            "parent_id": route_points.parent_id,
                            "point_type_id": route_points.point_type_id,
                            "route_point_name": route_points.route_point_name,
                            "route_point_short_name": route_points.route_point_short_name,
                            "svg_point": route_points.svg_point,
                        }
                        for route_points in route_points.routes_points
                    ]
                }
            )
        target_point = await self.store.mapAPI.get_route_point_by_id(route_point_id)
        if target_point is None:
            raise HTTPNotFound(resaon="Не существует запрашиваемого ресурса")
        point_type = await self.store.mapAPI.get_point_type_by_id(target_point.type_id)
        if self.request.user:
            user = self.request.user
            acceses = await self.store.userAPI.get_user_accesses(user.id)
            roles = [access.access_id.category_name for access in acceses.roles]
            if (
                (KEY_TYPES.ADMIN in roles)
                or (KEY_TYPES.OWNER in roles)
                or (KEY_TYPES.EDITOR in roles)
            ):
                return json_response(
                    data={
                        "id": target_point.id,
                        "parent_id": target_point.parent_id,
                        "created_time": target_point.created_time.strftime(
                                        "%Y-%m-%dT%H:%M:%S.%fZ"
                                    ),
                        "edited_time": target_point.edited_time.strftime(
                                        "%Y-%m-%dT%H:%M:%S.%fZ"
                                    ),
                        "type": {
                            "id": point_type.id,
                            "point_name": point_type.point_name,
                            "point_short_name": point_type.point_short_name,
                            "description": point_type.description,
                        },
                        "route_point_name": target_point.route_point_name,
                        "route_point_short_name": target_point.route_point_short_name,
                        "svg_point": target_point.svg_point,
                        "x_cord": target_point.x_cord,
                        "y_cord": target_point.y_cord,
                        "z_cord": target_point.z_cord,
                    }
                )
        return json_response(
            data={
                "id": target_point.id,
                "parent_id": target_point.parent_id,
                "type": {
                            "id": point_type.id,
                            "point_name": point_type.point_name,
                            "point_short_name": point_type.point_short_name,
                            "description": point_type.description,
                        },
                "route_point_name": target_point.route_point_name,
                "route_point_short_name": target_point.route_point_short_name,
                "description": target_point.description,
            }
        )

    @request_schema(NewRoutePointSchema)
    async def post(self):
        if self.request.user is None:
            raise HTTPUnauthorized(resaon="Вы не авторизованы")
        user = self.request.user
        acceses = await self.store.userAPI.get_user_accesses(user.id)
        if acceses is None:
            raise HTTPForbidden(resaon="Дотсуп к ресурсу запрещен")
        roles = [access.access_id.category_name for access in acceses.roles]
        if (KEY_TYPES.ADMIN not in roles) and (KEY_TYPES.OWNER not in roles):
            raise HTTPForbidden(resaon="Доступ к ресурсу запрещен")
        new_route_point = await self.store.mapAPI.createRoutePoint(
            route_point_name=self.data["route_point_name"],
            route_point_short_name=self.data["route_point_short_name"],
            parent_id=self.data.get("parent_id"),
            svg_point=self.data.get("svg_point"),
            object_id=self.data["object_id"],
            point_type_id=self.data["point_type_id"],
            x_cord=self.data["x"],
            y_cord=self.data["y"],
            z_cord=self.data["z"],
        )
        if new_route_point is None:
            raise HTTPBadRequest(resaon="Ошибка при создании")
        if self.store.map.working:
            await self.store.map.add_route(new_route_point)
        return json_response(
            data={
                "id": new_route_point.id,
                "route_point_name": new_route_point.route_point_name,
                "route_point_short_name": new_route_point.route_point_short_name,
                "parent_id": new_route_point.parent_id,
                "created_time": new_route_point.created_time.strftime(
                                        "%Y-%m-%dT%H:%M:%S.%fZ"
                                    ),
                "edited_time": new_route_point.edited_time.strftime(
                                        "%Y-%m-%dT%H:%M:%S.%fZ"
                                    ),
                "point_type_id": new_route_point.point_type_id,
                "object_id": new_route_point.object_id,
                "svg_point": new_route_point.svg_point,
                "x_cord": new_route_point.x_cord,
                "y_cord": new_route_point.y_cord,
                "z_cord": new_route_point.z_cord,
            }
        )

    @request_schema(UpdRoutePointSchema)
    async def put(self):
        if self.request.user is None:
            raise HTTPUnauthorized(resaon="Вы не авторизованы")
        user = self.request.user
        acceses = await self.store.userAPI.get_user_accesses(user.id)
        if acceses is None:
            raise HTTPForbidden(resaon="Доступ к ресурсу запрещен")
        roles = [access.access_id.category_name for access in acceses.roles]
        if (
            (KEY_TYPES.ADMIN not in roles)
            and (KEY_TYPES.OWNER not in roles)
            and (KEY_TYPES.EDITOR not in roles)
        ):
            raise HTTPForbidden(resaon="Доступ к ресурсу запрещен")
        try:
            route_point_id = int(self.request.rel_url.name)
        except:
            raise HTTPBadRequest(resaon="Не указан запрашиваеемый ресурс")
        old_route_point = await self.store.mapAPI.get_route_point_by_id(route_point_id)
        if old_route_point is None:
            raise HTTPNotFound(resaon="Запрашиваемый ресурс не существует")
        if self.data.get("route_point_name"):
            old_route_point.name = self.data.get("route_point_name")
        if self.data.get("svg_point"):
            old_route_point.description = self.data.get("svg_point")
        if self.data.get("route_point_short_name"):
            old_route_point.shortname = self.data.get("route_point_short_name")
        if self.data.get("x"):
            old_route_point.x_cord = self.data.get("x")
        if self.data.get("y"):
            old_route_point.y_cord = self.data.get("y")
        if self.data.get("z"):
            old_route_point.z_cord = self.data.get("z")
        upd_route_point = await self.store.mapAPI.update_RoutePointinfo(
            id=route_point_id,
            route_point_name=old_route_point.route_point_name,
            route_point_short_name=old_route_point.route_point_short_name,
            svg_point=old_route_point.svg_point,
            x_cord=old_route_point.x_cord,
            y_cord=old_route_point.y_cord,
            z_cord=old_route_point.z_cord,
        )
        if upd_route_point is None:
            raise HTTPBadRequest(resaon="Ошибка при обновлении")
        if self.store.map.working:
            await self.store.map.change_route(upd_route_point)
        return json_response(
            data={
                "id": upd_route_point.id,
                "route_point_name": upd_route_point.route_point_name,
                "route_point_short_name": upd_route_point.route_point_short_name,
                "parent_id": upd_route_point.parent_id,
                "created_time": upd_route_point.created_time.strftime(
                                        "%Y-%m-%dT%H:%M:%S.%fZ"
                                    ),
                "edited_time": upd_route_point.edited_time.strftime(
                                        "%Y-%m-%dT%H:%M:%S.%fZ"
                                    ),
                "object_id": upd_route_point.object_id,
                "point_type_id": upd_route_point.point_type_id,
                "svg_point": upd_route_point.svg_point,
                "x_cord": upd_route_point.x_cord,
                "y_cord": upd_route_point.y_cord,
                "z_cord": upd_route_point.z_cord,
            }
        )

    async def delete(self):
        if self.request.user is None:
            raise HTTPUnauthorized(resaon="Вы не авторизованы")
        user = self.request.user
        acceses = await self.store.userAPI.get_user_accesses(user.id)
        if acceses is None:
            raise HTTPForbidden(resaon="Доступ к ресурсу запрещен")
        roles = [access.access_id.category_name for access in acceses.roles]
        if (KEY_TYPES.ADMIN not in roles) and (KEY_TYPES.OWNER not in roles):
            raise HTTPForbidden(resaon="Доступ к ресурсу запрещен")
        try:
            route_point_id = int(self.request.rel_url.name)
        except:
            raise HTTPBadRequest(resaon="Запрашиваемый ресурс не указан")
        search_node = await self.store.mapAPI.get_route_point_by_id(route_point_id)
        if search_node is None:
            raise HTTPNotFound(resaon="Запрашиваемый ресурс не существует")
        result = await self.store.mapAPI.deleteRoutePoint(route_point_id)
        if not result:
            raise HTTPBadRequest(resaon="Ошибка при удалении")
        if self.store.map.working:
            await self.store.map.delete_route_point(route_point_id)
        return json_response(data={"result": "Успешное удаление"})


class PointConnectionView(CorsViewMixin, View):
    async def get(self):
        try:
            conn_id = int(self.request.rel_url.name)
        except:
            page = int(self.request.query.get("page", 1))
            if page < 1:
                raise HTTPBadRequest(resaon="Неверный параметр")
            node = int(self.request.query.get("node", 0))
            if node < 0:
                raise HTTPBadRequest(resaon="Неверный параметр")
            unlimited = int(self.request.query.get("unlimited", 0))
            if unlimited == 1:
                conns = await self.store.mapAPI.get_all_point_connections(page=None,limit=None)
      #      elif node:
      #          conns = await self.store.mapAPI.get_all_connections_of_node(node)
            else:
                conns = await self.store.mapAPI.get_all_point_connections(page=page, limit=10)
            if not conns:
                raise HTTPNotFound(resaon="Вы вышли за пределы списка соединений")
            return json_response(
                data={
                    "connections": [
                        {
                            "id": conn.id,
                            "route_point1_id": conn.route_point1_id,
                            "route_point2_id": conn.route_point2_id,
                            "route_distance": conn.route_distance,
                            "route_time": conn.route_time,
                            "weight_coefficient": conn.weight_coefficient,
                            "direction_1_to_2": conn.direction_1_to_2,
                            "direction_2_to_1": conn.direction_2_to_1,
                        }
                        for conn in conns.points_conns
                    ]
                }
            )
        target_conn = await self.store.mapAPI.get_point_connection_by_id(conn_id)
        if target_conn is None:
            raise HTTPNotFound(resaon="Запрашиваемый ресурс не существует")
        node1 = await self.store.mapAPI.get_route_point_by_id(target_conn.node1_id)
        node2 = await self.store.mapAPI.get_route_point_by_id(target_conn.node2_id)
        if self.request.user:
            user = self.request.user
            acceses = await self.store.userAPI.get_user_accesses(user.id)
            roles = [access.access_id.name for access in acceses.roles]
            if (
                (KEY_TYPES.ADMIN in roles)
                or (KEY_TYPES.OWNER in roles)
                or (KEY_TYPES.EDITOR in roles)
            ):
                return json_response(
                    data={
                        "id": target_conn.id,
                        "node1": {
                            "id": node1.id,
                            "parent_id": node1.parent_id,
                            "creator_id": node1.creator_id,
                            "created_time": node1.created_time.strftime(
                                        "%Y-%m-%dT%H:%M:%S.%fZ"
                                    ),
                            "editor_id": node1.editor_id,
                            "edited_time": node1.edited_time.strftime(
                                        "%Y-%m-%dT%H:%M:%S.%fZ"
                                    ),
                            "point_type_id": node1.point_type_id,
                            "object_id": node1.object_id,
                            "route_point_name": node1.route_point_name,
                            "route_point_short_name": node1.route_point_short_name,
                            "svg_point": node1.svg_point,
                            "x_cord": node1.x_cord,
                            "y_cord": node1.y_cord,
                            "z_cord": node1.z_cord,
                        },
                        "node2": {
                            "id": node2.id,
                            "parent_id": node2.parent_id,
                            "creator_id": node2.creator_id,
                            "created_time": node2.created_time.strftime(
                                        "%Y-%m-%dT%H:%M:%S.%fZ"
                                    ),
                            "editor_id": node2.editor_id,
                            "edited_time": node2.edited_time.strftime(
                                        "%Y-%m-%dT%H:%M:%S.%fZ"
                                    ),
                            "point_type_id": node2.point_type_id,
                            "object_id": node2.object_id,
                            "route_point_name": node2.route_point_name,
                            "route_point_short_name": node2.route_point_short_name,
                            "svg_point": node2.svg_point,
                            "x_cord": node2.x_cord,
                            "y_cord": node2.y_cord,
                            "z_cord": node2.z_cord,
                        },
                        "route_distance": target_conn.route_distance,
                        "route_time": target_conn.route_time,
                        "weight_coefficient": target_conn.weight_coefficient,
                    }
                )
        return json_response(
            data={
                "id": target_conn.id,
                "node1": {
                    "id": node1.id,
                    "parent_id": node1.parent_id,
                    "point_type_id": node1.point_type_id,
                    "object_id": node1.object_id,
                    "route_point_name": node1.route_point_name,
                    "route_point_short_name": node1.route_point_short_name,
                    "svg_point": node1.svg_point,
                },
                "node2": {
                    "id": node2.id,
                    "parent_id": node2.parent_id,
                    "point_type_id": node2.point_type_id,
                    "object_id": node1.object_id,
                    "route_point_name": node2.route_point_name,
                    "route_point_short_name": node2.route_point_short_name,
                    "svg_point": node2.svg_point,
                },
                "route_distance": target_conn.route_distance,
                "route_time": target_conn.route_time,
                "weight_coefficient": target_conn.weight_coefficient,
            }
        )

    @request_schema(NewPointConnSchema)
    async def post(self):
        if self.request.user is None:
            raise HTTPUnauthorized(resaon="Вы не авторизованы")
        user = self.request.user
        acceses = await self.store.userAPI.get_user_accesses(user.id)
        if acceses is None:
            raise HTTPForbidden(resaon="Доступ к запрашиваемому ресурсу запрещен")
        roles = [access.access_id.category_name for access in acceses.roles]
        if (KEY_TYPES.ADMIN not in roles) and (KEY_TYPES.OWNER not in roles):
            raise HTTPForbidden(resaon="Доступ к запрашиваемому ресурсу запрещен")
        if self.data["route_point1_id"] == self.data["route_point2_id"]:
            raise HTTPBadRequest(resaon='''Соединение на "само себя" ''')
        new_conn = await self.store.mapAPI.createConnection(
            route_point1_id=self.data["route_point1_id"],
            route_point2_id=self.data["route_point2_id"],
            route_distance=self.data["route_distance"],
            route_time=self.data["route_time"],
            weight_coefficient=self.data["weight_coefficient"],
        )
        if new_conn is None:
            raise HTTPBadRequest(resaon="Ошибка при создании")
        if self.store.map.working:
            await self.store.map.add_conn(new_conn)
        return json_response(
            data={
                "id":new_conn.id,
                "route_point1_id": new_conn.route_point1_id,
                "route_point2_id": new_conn.route_point2_id,
                "route_distance": new_conn.route_distance,
                "route_time": new_conn.route_time,
                "weight_coefficient": new_conn.weight_coefficient,
            }
        )

    @request_schema(UpdPointConnSchema)
    async def put(self):
        if self.request.user is None:
            raise HTTPUnauthorized(resaon="Вы не авторизованы")
        user = self.request.user
        acceses = await self.store.userAPI.get_user_accesses(user.id)
        if acceses is None:
            raise HTTPForbidden(resaon="Доступ к ресурсу запрещен")
        roles = [access.access_id.category_name for access in acceses.roles]
        if (
            (KEY_TYPES.ADMIN not in roles)
            and (KEY_TYPES.OWNER not in roles)
            and (KEY_TYPES.EDITOR not in roles)
        ):
            raise HTTPForbidden(resaon="Доступ к ресурсу запрещен")
        try:
            conn_id = int(self.request.rel_url.name)
        except:
            raise HTTPBadRequest(resaon="Не указан запршиваемый ресурс")
        old_conn = await self.store.mapAPI.get_point_connection_by_id(conn_id)
        if old_conn is None:
            raise HTTPNotFound(resaon="Запрашиваемый ресурс не существует")
        if self.data.get("route_distance"):
            old_conn.distance = self.data.get("route_distance")
        if self.data.get("weight_coefficient"):
            old_conn.t_weight = self.data.get("weight_coefficient")
        if self.data.get("route_time"):
            old_conn.time = self.data.get("route_time")
        upd_conn = await self.store.mapAPI.update_PointConninfo(
            id=conn_id,
            route_distance=old_conn.route_distance,
            route_time=old_conn.route_time,
            weight_coefficient=old_conn.weight_coefficient,
        )
        if upd_conn is None:
            raise HTTPBadRequest(resaon="Ошибка при изменении")
        if self.store.map.working:
            await self.store.map.change_conn(upd_conn)
        return json_response(
            data={
                "id":upd_conn.id,
                "route_point1_id": upd_conn.route_point1_id,
                "route_point2_id": upd_conn.route_point2_id,
                "route_distance": upd_conn.route_distance,
                "route_time": upd_conn.route_time,
                "weight_coefficient": upd_conn.weight_coefficient,
            }
        )

    async def delete(self):
        if self.request.user is None:
            raise HTTPUnauthorized(resaon="Вы не авторизованы")
        user = self.request.user
        acceses = await self.store.userAPI.get_user_accesses(user.id)
        if acceses is None:
            raise HTTPForbidden(resaon="Доступ к ресурсу запрещен")
        roles = [access.access_id.category_name for access in acceses.roles]
        if (KEY_TYPES.ADMIN not in roles) and (KEY_TYPES.OWNER not in roles):
            raise HTTPForbidden(resaon="Доступ к ресурсу запрещен")
        try:
            conn_id = int(self.request.rel_url.name)
        except:
            raise HTTPBadRequest(resaon="Не указан запрашиваемый ресурс")
        seacrh_conn = await self.store.mapAPI.get_point_connection_by_id(conn_id)
        if seacrh_conn is None:
            raise HTTPNotFound(resaon="Запрашиваемый ресурс не существует")
        result = await self.store.mapAPI.deletePointConnection(conn_id)
        if not result:
            raise HTTPBadRequest(resaon="Ошибка при удалении")
        if self.store.map.working:
            await self.store.map.delete_conn(conn_id,seacrh_conn.route_point1_id,seacrh_conn.route_point2_id)
        return json_response(data={"result": "Успешное удаление"})

class ObjectStatusView(CorsViewMixin, View):
    async def get(self):
        try:
            object_status_id = int(self.request.rel_url.name)
        except:
            page = int(self.request.query.get("page", 1))
            if page < 1:
                raise HTTPBadRequest(resaon="Неверный параметр")
            unlimited = int(self.request.query.get("unlimited", 0))
            if unlimited == 1:
                objects_statuses = await self.store.mapAPI.get_all_object_status(page=None,limit=None)
            else:
                objects_statuses = await self.store.mapAPI.get_all_object_status(page=page, limit=10)
            if not objects_statuses:
                raise HTTPNotFound(resaon="Вы вышли за границы списка")
            return json_response(
                data=[
                    {
                        "id": objects_status.id,
                        "object_status_name": objects_status.object_status_name,
                    }
                    for objects_status in objects_statuses.objects_status
                ]
            )
        search_object_status = await self.store.mapAPI.get_object_status_by_id(object_status_id)
        if search_object_status is None:
            raise HTTPNotFound(resaon="Не существует")
        return json_response(
            data={
                "id": search_object_status.id,
                "object_status_name": search_object_status.object_status_name,
            }
        )

    @request_schema(NewObjectStatusSchema)
    async def post(self):
        if self.request.user is None:
            raise HTTPUnauthorized(resaon="Нет авторизации")
        user = self.request.user
        acceses = await self.store.userAPI.get_user_accesses(user.id)
        if acceses is None:
            raise HTTPForbidden(resaon="Доступ к ресурсу запрещен")
        roles = [access.access_id.category_name for access in acceses.roles]
        if (KEY_TYPES.ADMIN not in roles) and (KEY_TYPES.OWNER not in roles):
            raise HTTPForbidden(resaon="Доступ к ресурсу запрещен")
        new_object_status = await self.store.mapAPI.createObjectStatus(
            object_status_name=self.data["object_status_name"],
        )
        if new_object_status is None:
            raise HTTPBadRequest(resaon="Ошибка при создании")
        return json_response(
            data={
                "id": new_object_status.id,
                "object_status_name": new_object_status.object_status_name,
            }
        )

    @request_schema(UpdObjectStatusSchema)
    async def put(self):
        if self.request.user is None:
            raise HTTPUnauthorized(resaon="Вы не авторизованы")
        user = self.request.user
        acceses = await self.store.userAPI.get_user_accesses(user.id)
        if acceses is None:
            raise HTTPForbidden(resaon="Доступ к ресурсу запрещен")
        roles = [access.access_id.category_name for access in acceses.roles]
        if (KEY_TYPES.ADMIN not in roles) and (KEY_TYPES.OWNER not in roles):
            raise HTTPForbidden(resaon="Доступ к ресурсу запрещен")
        try:
            object_status_id = int(self.request.rel_url.name)
        except:
            raise HTTPBadRequest(resaon="Не указан тип")
        search_object_status = await self.store.mapAPI.get_object_status_by_id(object_status_id)
        if search_object_status is None:
            raise HTTPNotFound(resaon="Нет такого объекта")
        if self.data.get("object_status_name"):
            search_object_status.object_status_name = self.data.get("object_status_name")
        upd_object_status = await self.store.mapAPI.update_ObjectStatusinfo(
            id=object_status_id,
            object_status_name=search_object_status.object_status_name,
        )
        if upd_object_status is None:
            raise HTTPBadRequest("Ошибка при изменении")
        return json_response(
            data={
                "id": upd_object_status.id,
                "object_status_name": upd_object_status.object_status_name,
            }
        )

    async def delete(self):
        if self.request.user is None:
            raise HTTPUnauthorized(resaon="Вы не авторизованы")
        user = self.request.user
        acceses = await self.store.userAPI.get_user_accesses(user.id)
        if acceses is None:
            raise HTTPForbidden(resaon="Доступ к ресурсу запрещен")
        roles = [access.access_id.category_name for access in acceses.roles]
        if (KEY_TYPES.ADMIN not in roles) and (KEY_TYPES.OWNER not in roles):
            raise HTTPForbidden(resaon="Доступ к ресурсу запрещен")
        try:
            object_status_id = int(self.request.rel_url.name)
        except:
            raise HTTPBadRequest(resaon="Нет указан ресурс")
        search_object = await self.store.mapAPI.get_object_status_by_id(object_status_id)
        if search_object is None:
            raise HTTPNotFound(resaon="Указанный ресурс не существует")
        result = await self.store.mapAPI.deleteObjectStatus(object_status_id)
        if not result:
            raise HTTPBadRequest(resaon="Ошибка при удалении")
        return json_response(data={"result": "Успешное удаление"})

class PointTypeView(CorsViewMixin, View):
    async def get(self):
        try:
            point_type_id = int(self.request.rel_url.name)
        except:
            page = int(self.request.query.get("page", 1))
            if page < 1:
                raise HTTPBadRequest(resaon="Неверный параметр")
            unlimited = int(self.request.query.get("unlimited", 0))
            if unlimited == 1:
                point_types = await self.store.mapAPI.get_all_point_types(page=None,limit=None)
            else:
                point_types = await self.store.mapAPI.get_all_point_types(page=page, limit=10)
            if not point_types:
                raise HTTPNotFound(resaon="Вы вышли за границы списка")
            return json_response(
                data=[
                    {
                        "id": point_type.id,
                        "point_name": point_type.point_name,
                        "point_short_name": point_type.point_short_name,
                        "description": point_type.description,
                    }
                    for point_type in point_types.points_types
                ]
            )
        search_point_type = await self.store.mapAPI.get_point_type_by_id(point_type_id)
        if search_point_type is None:
            raise HTTPNotFound(resaon="Не существует")
        return json_response(
            data={
                "id": search_point_type.id,
                "point_name": search_point_type.point_name,
                "point_short_name": search_point_type.point_short_name,
                "description": search_point_type.description,
            }
        )

    @request_schema(NewPointTypeSchema)
    async def post(self):
        if self.request.user is None:
            raise HTTPUnauthorized(resaon="Нет авторизации")
        user = self.request.user
        acceses = await self.store.userAPI.get_user_accesses(user.id)
        if acceses is None:
            raise HTTPForbidden(resaon="Доступ к ресурсу запрещен")
        roles = [access.access_id.category_name for access in acceses.roles]
        if (KEY_TYPES.ADMIN not in roles) and (KEY_TYPES.OWNER not in roles):
            raise HTTPForbidden(resaon="Доступ к ресурсу запрещен")
        new_point_type = await self.store.mapAPI.createPointType(
            point_name=self.data["point_name"],
            point_short_name=self.data["point_short_name"],
            description=self.data["description"],
        )
        if new_point_type is None:
            raise HTTPBadRequest(resaon="Ошибка при создании")
        return json_response(
            data={
                "id": new_point_type.id,
                "point_name": new_point_type.point_name,
                "point_short_name": new_point_type.point_short_name,
                "description": new_point_type.description,
            }
        )

    @request_schema(UpdPointTypeSchema)
    async def put(self):
        if self.request.user is None:
            raise HTTPUnauthorized(resaon="Вы не авторизованы")
        user = self.request.user
        acceses = await self.store.userAPI.get_user_accesses(user.id)
        if acceses is None:
            raise HTTPForbidden(resaon="Доступ к ресурсу запрещен")
        roles = [access.access_id.category_name for access in acceses.roles]
        if (KEY_TYPES.ADMIN not in roles) and (KEY_TYPES.OWNER not in roles):
            raise HTTPForbidden(resaon="Доступ к ресурсу запрещен")
        try:
            point_type_id = int(self.request.rel_url.name)
        except:
            raise HTTPBadRequest(resaon="Не указан тип")
        search_point_type = await self.store.mapAPI.get_point_type_by_id(point_type_id)
        if search_point_type is None:
            raise HTTPNotFound(resaon="Нет такого объекта")
        if self.data.get("point_name"):
            search_point_type.point_name = self.data.get("point_name")
        if self.data.get("point_short_name"):
            search_point_type.point_short_name = self.data.get("point_short_name")
        if self.data.get("description"):
            search_point_type.description = self.data.get("description")
        upd_point_type = await self.store.mapAPI.update_PointTypeinfo(
            id=point_type_id,
            point_name=search_point_type.point_name,
            point_short_name=search_point_type.point_short_name,
            description=search_point_type.description,
        )
        if upd_point_type is None:
            raise HTTPBadRequest("Ошибка при изменении")
        return json_response(
            data={
                "id": upd_point_type.id,
                "point_name": upd_point_type.point_name,
                "point_short_name": upd_point_type.point_short_name,
                "description": upd_point_type.description,
            }
        )

    async def delete(self):
        if self.request.user is None:
            raise HTTPUnauthorized(resaon="Вы не авторизованы")
        user = self.request.user
        acceses = await self.store.userAPI.get_user_accesses(user.id)
        if acceses is None:
            raise HTTPForbidden(resaon="Доступ к ресурсу запрещен")
        roles = [access.access_id.category_name for access in acceses.roles]
        if (KEY_TYPES.ADMIN not in roles) and (KEY_TYPES.OWNER not in roles):
            raise HTTPForbidden(resaon="Доступ к ресурсу запрещен")
        try:
            point_type_id = int(self.request.rel_url.name)
        except:
            raise HTTPBadRequest(resaon="Нет указан ресурс")
        search_point_type = await self.store.mapAPI.get_point_type_by_id(point_type_id)
        if search_point_type is None:
            raise HTTPNotFound(resaon="Указанный ресурс не существует")
        result = await self.store.mapAPI.deletePointType(point_type_id)
        if not result:
            raise HTTPBadRequest(resaon="Ошибка при удалении")
        return json_response(data={"result": "Успешное удаление"})

class ObjectTypeView(CorsViewMixin, View):
    async def get(self):
        try:
            object_type_id = int(self.request.rel_url.name)
        except:
            page = int(self.request.query.get("page", 1))
            if page < 1:
                raise HTTPBadRequest(resaon="Неверный параметр")
            unlimited = int(self.request.query.get("unlimited", 0))
            if unlimited == 1:
                object_types = await self.store.mapAPI.get_all_object_types(page=None,limit=None)
            else:
                object_types = await self.store.mapAPI.get_all_object_types(page=page, limit=10)
            if not object_types:
                raise HTTPNotFound(resaon="Вы вышли за границы списка")
            return json_response(
                data=[
                    {
                        "id": object_type.id,
                        "parent_id": object_type.parent_id,
                        "object_type_name": object_type.object_type_name,
                        "object_type_short_name": object_type.object_type_short_name,
                        "description_object_type": object_type.description_object_type,

                    }
                    for object_type in object_types.objects_types
                ]
            )
        search_object_type = await self.store.mapAPI.get_object_type_by_id(object_type_id)
        if search_object_type is None:
            raise HTTPNotFound(resaon="Не существует")
        return json_response(
            data={
                "id": search_object_type.id,
                "parent_id": search_object_type.parent_id,
                "object_type_name": search_object_type.object_type_name,
                "object_type_short_name": search_object_type.object_type_short_name,
                "description_object_type": search_object_type.description_object_type,
            }
        )

    @request_schema(NewObjectTypeSchema)
    async def post(self):
        if self.request.user is None:
            raise HTTPUnauthorized(resaon="Нет авторизации")
        user = self.request.user
        acceses = await self.store.userAPI.get_user_accesses(user.id)
        if acceses is None:
            raise HTTPForbidden(resaon="Доступ к ресурсу запрещен")
        roles = [access.access_id.category_name for access in acceses.roles]
        if (KEY_TYPES.ADMIN not in roles) and (KEY_TYPES.OWNER not in roles):
            raise HTTPForbidden(resaon="Доступ к ресурсу запрещен")
        new_object_type = await self.store.mapAPI.createObjectType(
            parent_id=self.data["parent_id"],
            object_type_name=self.data["object_type_name"],
            object_type_short_name=self.data["object_type_short_name"],
            description_object_type=self.data["description_object_type"],
        )
        if new_object_type is None:
            raise HTTPBadRequest(resaon="Ошибка при создании")
        return json_response(
            data={
                "id": new_object_type.id,
                "parent_id": new_object_type.parent_id,
                "object_type_name": new_object_type.object_type_name,
                "object_type_short_name": new_object_type.object_type_short_name,
                "description_object_type": new_object_type.description_object_type,
            }
        )

    @request_schema(UpdObjecTypeSchema)
    async def put(self):
        if self.request.user is None:
            raise HTTPUnauthorized(resaon="Вы не авторизованы")
        user = self.request.user
        acceses = await self.store.userAPI.get_user_accesses(user.id)
        if acceses is None:
            raise HTTPForbidden(resaon="Доступ к ресурсу запрещен")
        roles = [access.access_id.category_name for access in acceses.roles]
        if (KEY_TYPES.ADMIN not in roles) and (KEY_TYPES.OWNER not in roles):
            raise HTTPForbidden(resaon="Доступ к ресурсу запрещен")
        try:
            object_type_id = int(self.request.rel_url.name)
        except:
            raise HTTPBadRequest(resaon="Не указан тип")
        search_object_type = await self.store.mapAPI.get_object_type_by_id(object_type_id)
        if search_object_type is None:
            raise HTTPNotFound(resaon="Нет такого объекта")
        if self.data.get("object_type_name"):
            search_object_type.object_type_name = self.data.get("object_type_name")
        if self.data.get("object_type_short_name"):
            search_object_type.object_type_short_name = self.data.get("object_type_short_name")
        if self.data.get("description_object_type"):
            search_object_type.description_object_type = self.data.get("description_object_type")
        upd_object_type = await self.store.mapAPI.update_ObjectTypeinfo(
            id=object_type_id,
            object_type_name=search_object_type.object_type_name,
            object_type_short_name=search_object_type.object_type_short_name,
            description_object_type=search_object_type.description_object_type,
        )
        if upd_object_type is None:
            raise HTTPBadRequest("Ошибка при изменении")
        return json_response(
            data={
                "id": upd_object_type.id,
                "object_type_name": upd_object_type.object_type_name,
                "object_type_short_name": upd_object_type.object_type_short_name,
                "description_object_type": upd_object_type.description_object_type,
            }
        )

    async def delete(self):
        if self.request.user is None:
            raise HTTPUnauthorized(resaon="Вы не авторизованы")
        user = self.request.user
        acceses = await self.store.userAPI.get_user_accesses(user.id)
        if acceses is None:
            raise HTTPForbidden(resaon="Доступ к ресурсу запрещен")
        roles = [access.access_id.category_name for access in acceses.roles]
        if (KEY_TYPES.ADMIN not in roles) and (KEY_TYPES.OWNER not in roles):
            raise HTTPForbidden(resaon="Доступ к ресурсу запрещен")
        try:
            object_type_id = int(self.request.rel_url.name)
        except:
            raise HTTPBadRequest(resaon="Нет указан ресурс")
        search_point_type = await self.store.mapAPI.get_object_type_by_id(object_type_id)
        if search_point_type is None:
            raise HTTPNotFound(resaon="Указанный ресурс не существует")
        result = await self.store.mapAPI.deleteObjectType(object_type_id)
        if not result:
            raise HTTPBadRequest(resaon="Ошибка при удалении")
        return json_response(data={"result": "Успешное удаление"})


class ObjectDrawingView(CorsViewMixin, View):
    async def get(self):
        try:
            object_drawing_id = int(self.request.rel_url.name)
        except:
            page = int(self.request.query.get("page", 1))
            if page < 1:
                raise HTTPBadRequest(resaon="Неверный параметр")
            unlimited = int(self.request.query.get("unlimited", 0))
            if unlimited == 1:
                object_drawings = await self.store.mapAPI.get_all_object_drawings(page=None,limit=None)
            else:
                object_drawings = await self.store.mapAPI.get_all_object_drawings(page=page, limit=10)
            if not object_drawings:
                raise HTTPNotFound(resaon="Вы вышли за границы списка")
            return json_response(
                data=[
                    {
                        "id": object_drawing.id,
                        "parent_id": object_drawing.parent_id,
                        "editor_id": object_drawing.editor_id,
                        "creator_id": object_drawing.creator_id,
                        "created_time": object_drawing.created_time.strftime(
                            "%Y-%m-%dT%H:%M:%S.%fZ"
                        ),
                        "edited_time": object_drawing.edited_time.strftime(
                            "%Y-%m-%dT%H:%M:%S.%fZ"
                        ),
                        "object_drawing_name": object_drawing.object_drawing_name,
                        "object_drawing_short_name": object_drawing.object_drawing_short_name,
                        "object_ref": object_drawing.object_ref,
                        "plan_ref": object_drawing.plan_ref,
                        "drawing_scale": object_drawing.drawing_scale,
                        "height": object_drawing.height,
                        "object_type_id": object_drawing.object_type_id,

                    }
                    for object_drawing in object_drawings.objects_drawings
                ]
            )
        search_object_drawing = await self.store.mapAPI.get_object_drawing_by_id(object_drawing_id)
        if search_object_drawing is None:
            raise HTTPNotFound(resaon="Не существует")
        return json_response(
            data={
                "id": search_object_drawing.id,
                "parent_id": search_object_drawing.parent_id,
                "object_drawing_name": search_object_drawing.object_drawing_name,
                "object_drawing_short_name": search_object_drawing.object_drawing_short_name,
                "object_ref": search_object_drawing.object_ref,
                "plan_ref": search_object_drawing.plan_ref,
                "drawing_scale": search_object_drawing.drawing_scale,
                "height": search_object_drawing.height,
                "object_type_id": search_object_drawing.object_type_id,
            }
        )

    @request_schema(NewObjectDrawingsSchema)
    async def post(self):
        if self.request.user is None:
            raise HTTPUnauthorized(resaon="Нет авторизации")
        user = self.request.user
        acceses = await self.store.userAPI.get_user_accesses(user.id)
        if acceses is None:
            raise HTTPForbidden(resaon="Доступ к ресурсу запрещен")
        roles = [access.access_id.category_name for access in acceses.roles]
        if (KEY_TYPES.ADMIN not in roles) and (KEY_TYPES.OWNER not in roles):
            raise HTTPForbidden(resaon="Доступ к ресурсу запрещен")
        new_object_drawing = await self.store.mapAPI.createObjectDrawing(
            parent_id=self.data["parent_id"],
            object_drawing_name=self.data["object_drawing_name"],
            object_drawing_short_name=self.data["object_drawing_short_name"],
            object_ref=self.data["object_ref"],
            plan_ref=self.data["plan_ref"],
            drawing_scale=self.data["drawing_scale"],
            height=self.data["height"],
            object_type_id=self.data["object_type_id"],
        )
        if new_object_drawing is None:
            raise HTTPBadRequest(resaon="Ошибка при создании")
        return json_response(
            data={
                "id": new_object_drawing.id,
                "parent_id": new_object_drawing.parent_id,
                "object_drawing_name": new_object_drawing.object_drawing_name,
                "object_drawing_short_name": new_object_drawing.object_drawing_short_name,
                "object_ref": new_object_drawing.object_ref,
                "plan_ref": new_object_drawing.plan_ref,
                "drawing_scale": new_object_drawing.drawing_scale,
                "height": new_object_drawing.height,
                "object_type_id": new_object_drawing.object_type_id,
            }
        )

    @request_schema(UpdObjectDrawingsSchema)
    async def put(self):
        if self.request.user is None:
            raise HTTPUnauthorized(resaon="Вы не авторизованы")
        user = self.request.user
        acceses = await self.store.userAPI.get_user_accesses(user.id)
        if acceses is None:
            raise HTTPForbidden(resaon="Доступ к ресурсу запрещен")
        roles = [access.access_id.category_name for access in acceses.roles]
        if (KEY_TYPES.ADMIN not in roles) and (KEY_TYPES.OWNER not in roles):
            raise HTTPForbidden(resaon="Доступ к ресурсу запрещен")
        try:
            object_drawing_id = int(self.request.rel_url.name)
        except:
            raise HTTPBadRequest(resaon="Не указан тип")
        search_object_drawing = await self.store.mapAPI.get_object_drawing_by_id(object_drawing_id)
        if search_object_drawing is None:
            raise HTTPNotFound(resaon="Нет такого объекта")
        if self.data.get("object_drawing_name"):
            search_object_drawing.object_drawing_name = self.data.get("object_drawing_name")
        if self.data.get("object_drawing_short_name"):
            search_object_drawing.description_object_type = self.data.get("description_object_type")
        if self.data.get("object_ref"):
            search_object_drawing.object_ref = self.data.get("object_ref")
        if self.data.get("plan_ref"):
            search_object_drawing.plan_ref = self.data.get("plan_ref")
        if self.data.get("drawing_scale"):
            search_object_drawing.drawing_scale = self.data.get("drawing_scale")
        if self.data.get("height"):
            search_object_drawing.height = self.data.get("height")
        upd_object_drawing = await self.store.mapAPI.update_ObjectDrawinginfo(
            id=object_drawing_id,
            object_drawing_name=search_object_drawing.object_type_name,
            object_drawing_short_name=search_object_drawing.object_type_short_name,
            parent_id=search_object_drawing.parent_id,
            creator_id=search_object_drawing.user_id,
            editor_id=search_object_drawing.user_id,
            object_type_id=search_object_drawing.object_type_id,
            object_ref=search_object_drawing.object_ref,
            plan_ref=search_object_drawing.plan_ref,
            drawing_scale=search_object_drawing.drawing_scale,
            height=search_object_drawing.height,
            created_time=search_object_drawing.datetime.utcnow(),
            edited_time=search_object_drawing.datetime.utcnow(),
        )
        if upd_object_drawing is None:
            raise HTTPBadRequest("Ошибка при изменении")
        return json_response(
            data={
                "id": upd_object_drawing.id,
                "object_drawing_name": upd_object_drawing.object_drawing_name,
                "object_drawing_short_name": upd_object_drawing.object_drawing_short_name,
                "object_ref": upd_object_drawing.object_ref,
                "plan_ref": upd_object_drawing.plan_ref,
                "drawing_scale": upd_object_drawing.drawing_scale,
                "height": upd_object_drawing.height,
            }
        )

    async def delete(self):
        if self.request.user is None:
            raise HTTPUnauthorized(resaon="Вы не авторизованы")
        user = self.request.user
        acceses = await self.store.userAPI.get_user_accesses(user.id)
        if acceses is None:
            raise HTTPForbidden(resaon="Доступ к ресурсу запрещен")
        roles = [access.access_id.category_name for access in acceses.roles]
        if (KEY_TYPES.ADMIN not in roles) and (KEY_TYPES.OWNER not in roles):
            raise HTTPForbidden(resaon="Доступ к ресурсу запрещен")
        try:
            object_drawing_id = int(self.request.rel_url.name)
        except:
            raise HTTPBadRequest(resaon="Нет указан ресурс")
        search_object_drawing = await self.store.mapAPI.get_object_drawing_by_id(object_drawing_id)
        if search_object_drawing is None:
            raise HTTPNotFound(resaon="Указанный ресурс не существует")
        result = await self.store.mapAPI.deleteObjectDrawing(object_drawing_id)
        if not result:
            raise HTTPBadRequest(resaon="Ошибка при удалении")
        return json_response(data={"result": "Успешное удаление"})