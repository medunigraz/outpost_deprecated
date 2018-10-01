from rest_framework_extensions.key_constructor import bits
from rest_framework_extensions.key_constructor.constructors import DefaultKeyConstructor

from outpost.base.key_constructors import UpdatedAtKeyBit


class PersonKeyConstructor(DefaultKeyConstructor):
    unique_view_id = bits.UniqueMethodIdKeyBit()
    format = bits.FormatKeyBit()
    route = bits.QueryParamsKeyBit()


class DistributionListKeyConstructor(DefaultKeyConstructor):
    unique_view_id = bits.UniqueMethodIdKeyBit()
    format = bits.FormatKeyBit()
    route = bits.QueryParamsKeyBit()
