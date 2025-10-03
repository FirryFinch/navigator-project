from app.web.app import Application

from app.map.views import ObjectView, ObjectDrawingView, ObjectTypeView, PointTypeView, ObjectStatusView, PointConnectionView, RoutePointView, NavigateView, StartView


def register_urls(application: Application):

    application.router.add_view("/map/conn/", PointConnectionView)
    application.router.add_view("/map/conn/{conn_id}", PointConnectionView)
    application.router.add_view("/map/node/", RoutePointView)
    application.router.add_view("/map/node/{route_point_id}", RoutePointView)
    application.router.add_view("/map/route/type/", PointTypeView)
    application.router.add_view("/map/route/type/{point_type_id}", PointTypeView)
    application.router.add_view("/map/object/type", ObjectTypeView)
    application.router.add_view("/map/object/type/{object_type_id}", ObjectTypeView)
    application.router.add_view("/map/object/drawing", ObjectDrawingView)
    application.router.add_view("/map/object/drawing/{object_drawing_id}", ObjectDrawingView)
    application.router.add_view("/map/object/status", ObjectStatusView)
    application.router.add_view("/map/object/status/{id}", ObjectStatusView)
    application.router.add_view("/map/object/", ObjectView)
    application.router.add_view("/map/object/{object_id}", ObjectView)
    application.router.add_view("/map/navigate", NavigateView)
    application.router.add_view("/map/start", StartView)
