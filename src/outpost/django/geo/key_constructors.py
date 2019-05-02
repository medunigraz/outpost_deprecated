from rest_framework_extensions.key_constructor import bits
from rest_framework_extensions.key_constructor.constructors import DefaultKeyConstructor

from outpost.django.base.key_constructors import UpdatedAtKeyBit


class RoutingEdgeListKeyConstructor(DefaultKeyConstructor):
    route = bits.QueryParamsKeyBit(['from', 'to', 'accessible'])


class BackgroundListKeyConstructor(DefaultKeyConstructor):
    list_sql = bits.ListSqlQueryKeyBit()
    updated_at = UpdatedAtKeyBit()


class EdgeListKeyConstructor(DefaultKeyConstructor):
    list_sql = bits.ListSqlQueryKeyBit()
    updated_at = UpdatedAtKeyBit()


class NodeListKeyConstructor(DefaultKeyConstructor):
    list_sql = bits.ListSqlQueryKeyBit()
    updated_at = UpdatedAtKeyBit()


class RoomListKeyConstructor(NodeListKeyConstructor):
    pass


class DoorListKeyConstructor(NodeListKeyConstructor):
    pass


class FloorListKeyConstructor(NodeListKeyConstructor):
    pass


class BuildingListKeyConstructor(NodeListKeyConstructor):
    pass


class PointOfInterestInstanceListKeyConstructor(NodeListKeyConstructor):
    pass


class PointOfInterestListKeyConstructor(DefaultKeyConstructor):
    list_sql = bits.ListSqlQueryKeyBit()
    updated_at = UpdatedAtKeyBit()
