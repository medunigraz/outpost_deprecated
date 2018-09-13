from rest_framework.serializers import (
    ModelSerializer,
    PrimaryKeyRelatedField,
    SerializerMethodField,
)

from . import models


class RoomCategorySerializer(ModelSerializer):
    class Meta:
        model = models.RoomCategory
        fields = '__all__'


class FloorSerializer(ModelSerializer):
    class Meta:
        model = models.Floor
        exclude = (
            'short',
        )


class BuildingSerializer(ModelSerializer):
    class Meta:
        model = models.Building
        fields = '__all__'


class RoomSerializer(ModelSerializer):
    category = RoomCategorySerializer()
    floor = FloorSerializer()
    building = BuildingSerializer()

    class Meta:
        model = models.Room
        exclude = (
            'area',
            'height',
        )


class FunctionSerializer(ModelSerializer):
    class Meta:
        model = models.Function
        fields = '__all__'


class OrganizationSerializer(ModelSerializer):
    persons = PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = models.Organization
        fields = '__all__'


class PersonSerializer(ModelSerializer):
    room = RoomSerializer()

    class Meta:
        model = models.Person
        exclude = (
            'username',
            'avatar_private',
            'hash',
        )


class AuthenticatedPersonSerializer(ModelSerializer):
    room = RoomSerializer()
    avatar = SerializerMethodField()

    class Meta:
        model = models.Person
        exclude = (
            'username',
            'hash',
            'avatar_private',
        )

    def get_avatar(self, obj):
        request = self.context.get('request')
        path = obj.avatar_private_url()
        if request:
            return request.build_absolute_uri(path)
        return path


class PersonOrganizationFunctionSerializer(ModelSerializer):
    person = PersonSerializer()
    organization = OrganizationSerializer()
    function = FunctionSerializer()

    class Meta:
        model = models.PersonOrganizationFunction
        fields = '__all__'


class PersonNameSerializer(ModelSerializer):

    class Meta:
        model = models.Person
        exclude = (
            'username',
            'room',
        )


class DistributionListSerializer(ModelSerializer):

    class Meta:
        model = models.DistributionList
        fields = '__all__'


class CourseSerializer(ModelSerializer):

    class Meta:
        model = models.Course
        fields = (
            'id',
            'name',
            'category',
            'year',
            'semester',
        )


class CourseGroupSerializer(ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = models.CourseGroup
        fields = (
            'id',
            'course',
            'name',
        )


class CourseGroupTermSerializer(ModelSerializer):
    coursegroup = CourseGroupSerializer()
    person = PersonSerializer()
    room = RoomSerializer()

    class Meta:
        model = models.CourseGroupTerm
        fields = (
            'id',
            'coursegroup',
            'person',
            'start',
            'end',
            'room',
            'title',
            'term',
        )


class EventSerializer(ModelSerializer):
    building = BuildingSerializer()
    room = RoomSerializer()

    class Meta:
        model = models.Event
        fields = '__all__'


class BulletinSerializer(ModelSerializer):

    class Meta:
        model = models.Bulletin
        fields = '__all__'
