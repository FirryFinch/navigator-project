class PointType:

    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.proto = []


class RoutePoint:

    def __init__(
        self,
        id: int,
        typePoint: PointType,
        x: float,
        y: float,
        z: float,
        depth: int,
        route_point_name: str
    ):
        self.id = id
        self.type = typePoint
        self.x = x
        self.y = y
        self.z = z
        self.conns = dict()
        self.depth = depth
        self.route_point_name = route_point_name

    def __lt__(self, other):
        return self.id < other.id


class Connection:

    def __init__(self, id: int, route_distance: float, route_time: float, weight_coefficient: float):
        self.id = id
        self.route_distance = route_distance
        self.route_time = route_time
        self.weight_coefficient = weight_coefficient


class RouteNode:

    def __init__(
        self, target_distance: float, start_distance: float, node: RoutePoint, previous
    ):
        self.target_distance = target_distance
        self.start_distance = start_distance
        self.current = node
        self.previous = previous

    def __lt__(self, other):
        if self.target_distance+self.start_distance != other.target_distance+self.start_distance:
            return self.target_distance+self.start_distance < other.target_distance+self.start_distance
        return self.current < other.current



