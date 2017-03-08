from rest_framework_extensions.key_constructor import bits
from rest_framework_extensions.key_constructor.constructors import DefaultKeyConstructor


class RoutingEdgeKeyConstructor(DefaultKeyConstructor):
    unique_method_id = bits.UniqueMethodIdKeyBit()
    format = bits.FormatKeyBit()
    language = bits.LanguageKeyBit()
    route = bits.QueryParamsKeyBit(['from', 'to', 'accessible'])
