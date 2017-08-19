from drf_haystack.serializers import HaystackSerializer
from rest_framework.serializers import (
    IntegerField,
    SerializerMethodField,
)

from outpost.geo import search_indexes as geo
from outpost.structure import search_indexes as structure


class AutocompleteSerializer(HaystackSerializer):
    id = IntegerField(source='pk')
    ctype = SerializerMethodField()

    class Meta:
        index_classes = [
            geo.RoomIndex,
            structure.OrganizationIndex,
            structure.PersonIndex,
        ]
        fields = [
            'presentation',
            'id',
            'ctype',
            'level_id',
            'room_id',
            'autocomplete',
        ]
        ignore_fields = [
            'text',
            'autocomplete',
        ]
        field_aliases = {
            'q': 'autocomplete',
        }

    def get_ctype(self, obj):
        return obj.content_type()
