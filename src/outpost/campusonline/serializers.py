from rest_framework.serializers import ModelSerializer

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
    class Meta:
        model = models.Organization
        fields = '__all__'


class PersonSerializer(ModelSerializer):
    room = RoomSerializer()

    class Meta:
        model = models.Person
        exclude = (
            'username',
        )


class PersonNameSerializer(ModelSerializer):

    class Meta:
        model = models.Person
        exclude = (
            'username',
            'room',
        )


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
