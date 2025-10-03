import typing
import gc
import math
import heapq
from app.map_module.node import PointType, RoutePoint, Connection, RouteNode
from app.map_module.dataclasses import KEY_TYPES
from app.map.dataclasses import PointConnectionDC, RoutePointDC


if typing.TYPE_CHECKING:
    from app.web.app import Application


class Map:

    def __init__(self, app: "Application"):
        self.app = app
        self.types = dict()
        self.nodes = dict()
        self.all_point_cones = dict()
        self.exits = dict()
        self.exits_list = set()
        self.working = False

    async def start(self):
        point_types = await self.app.store.mapAPI.get_all_point_types(page=None, limit=None)
        for point_type in point_types.points_types:
            self.types[f"{point_type.id}"] = PointType(point_type.id, point_type.point_name)
        del point_types
        gc.collect()
        route_points = await self.app.store.mapAPI.get_all_route_point(page=None, limit=None)
        if route_points:
            for route_point in route_points.routes_points:
                    self.nodes[f"{route_point.id}"] = RoutePoint(
                        id=route_point.id,
                        typePoint=self.types[f"{route_point.point_type_id}"],
                        x=route_point.x_cord,
                        y=route_point.y_cord,
                        z=route_point.z_cord,
                        depth=1,
                        route_point_name=route_point.route_point_name,
                    )
        del route_points
        gc.collect()
        for node_id, node in self.nodes.items():
            conns = await self.app.store.mapAPI.get_all_point_connections_of_node(int(node_id))
            if conns:
                for conn in conns.points_conns:
                    self.all_point_cones[f"{conn.id}"] = Connection(
                        id=conn.id,
                        route_distance=conn.route_distance,
                        weight_coefficient=conn.weight_coefficient,
                        route_time=conn.route_time,
                    )
                    if conn.route_point1_id == int(node_id):
                        node.conns[f"{conn.route_point2_id}"] = self.all_point_cones[f"{conn.id}"]
                    else:
                        node.conns[f"{conn.route_point1_id}"] = self.all_point_cones[f"{conn.id}"]
        del conns
        gc.collect()
        self.working = True

    async def __go_up(self, target_class: str, route_point: RoutePoint) -> RoutePoint | None:
        current_route_point = route_point
        while current_route_point.type.name != target_class:
            current_route_point = current_route_point.parent
        if current_route_point.type.name == target_class:
            return current_route_point
        return None

    @staticmethod
    def __calculate_distance(current: RoutePoint, target: RoutePoint) -> float:
        return math.sqrt(
            (target.x - current.x)**2
            + (target.y - current.y)**2
            + (target.z - current.z)**2
        )

    async def __navigate_building(self, start_node: int, target_node: int):
        start = self.nodes[f"{start_node}"]
        target = self.nodes[f"{target_node}"]

        to_visit = []
        visited = set()

        heapq.heappush(
            to_visit,
            RouteNode(
                target_distance=self.__calculate_distance(start, target),
                start_distance=0,
                node=start,
                previous=-1,
            ),
        )

        while to_visit:
            current_node = heapq.heappop(to_visit)

            if current_node.current.id == target.id:
                result = list()
                length = current_node.start_distance
                while current_node.previous != -1:
                    result.append(current_node.current)
                    current_node = current_node.previous
                else:
                    result.append(current_node.current)
                return {"result": result[::-1], "length": length}

            visited.add(current_node.current.id)

            for key_node_id, conn_value in current_node.current.conns.items():
                if int(key_node_id) in visited:
                    continue

                if elem := next(
                    (
                        element
                        for element in to_visit
                        if element.current.id == int(key_node_id)
                    ),
                    None,
                ):
                    if (
                        current_node.start_distance + conn_value.route_distance
                        < elem.start_distance
                    ):
                        elem.start_distance = (
                            current_node.start_distance + conn_value.route_distance
                        )
                        elem.previous = current_node
                else:
                    heapq.heappush(
                        to_visit,
                        RouteNode(
                            self.__calculate_distance(
                                self.nodes[f"{key_node_id}"], target
                            ),
                            current_node.start_distance + conn_value.route_distance,
                            self.nodes[f"{key_node_id}"],
                            current_node,
                        ),
                    )

    async def navigate_main(self, start_node: int, target_node: int):
        start = self.nodes[f"{start_node}"]
        target = self.nodes[f"{target_node}"]
        result = await self.__navigate_building(start_node, target_node)
        return result["result"]
