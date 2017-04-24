from rest_framework_extensions.key_constructor import bits
from rest_framework_extensions.key_constructor.constructors import (
    DefaultKeyConstructor,
)


class RoutingEdgeListKeyConstructor(DefaultKeyConstructor):
    route = bits.QueryParamsKeyBit(['from', 'to', 'accessible'])


class EdgeListKeyConstructor(DefaultKeyConstructor):
    list_sql = bits.ListSqlQueryKeyBit()


class NodeListKeyConstructor(DefaultKeyConstructor):
    list_sql = bits.ListSqlQueryKeyBit()


class RoomListKeyConstructor(NodeListKeyConstructor):
    pass


class DoorListKeyConstructor(NodeListKeyConstructor):
    pass


class FloorListKeyConstructor(NodeListKeyConstructor):
    pass


class BuildingListKeyConstructor(NodeListKeyConstructor):
    pass
