from django.urls import reverse
from rest_flex_fields import FlexFieldsModelSerializer
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


class FunctionSerializer(FlexFieldsModelSerializer):
    '''
    ## Expansions

    To activate relation expansion add the desired fields as a comma separated
    list to the `expand` query parameter like this:

        ?expand=<field>,<field>,<field>,...

    The following relational fields can be expanded:

     * `persons`

    '''

    @property
    def expandable_fields(self):
        serializer = 'PersonSerializer'
        request = self.context.get('request', None)
        if request:
            if request.user:
                if request.user.is_authenticated():
                    serializer = 'AuthenticatedPersonSerializer'
        return {
            'persons': (
                f'outpost.django.campusonline.serializers.{serializer}',
                {
                    'source': 'persons',
                    'many': True
                }
            ),
        }

    class Meta:
        model = models.Function
        fields = '__all__'


class OrganizationSerializer(FlexFieldsModelSerializer):
    '''
    ## Expansions

    To activate relation expansion add the desired fields as a comma separated
    list to the `expand` query parameter like this:

        ?expand=<field>,<field>,<field>,...

    The following relational fields can be expanded:

     * `persons`

    '''
    persons = PrimaryKeyRelatedField(many=True, read_only=True)

    @property
    def expandable_fields(self):
        serializer = 'PersonSerializer'
        request = self.context.get('request', None)
        if request:
            if request.user:
                if request.user.is_authenticated():
                    serializer = 'AuthenticatedPersonSerializer'
        return {
            'persons': (
                f'outpost.django.campusonline.serializers.{serializer}',
                {
                    'source': 'persons',
                    'many': True
                }
            ),
        }

    class Meta:
        model = models.Organization
        fields = '__all__'


class PersonSerializer(FlexFieldsModelSerializer):
    '''
    ## Expansions

    To activate relation expansion add the desired fields as a comma separated
    list to the `expand` query parameter like this:

        ?expand=<field>,<field>,<field>,...

    The following relational fields can be expanded:

     * `functions` <i class="glyphicon glyphicon-lock"></i>
     * `organizations` <i class="glyphicon glyphicon-lock"></i>

    '''
    room = RoomSerializer()

    class Meta:
        model = models.Person
        exclude = (
            'username',
            'avatar_private',
            'hash',
            'email',
            'functions',
            'organizations',
            'sex',
        )


class AuthenticatedPersonSerializer(PersonSerializer):
    avatar = SerializerMethodField()

    expandable_fields = {
        'functions': (
            'outpost.django.campusonline.serializers.FunctionSerializer',
            {
                'source': 'functions',
                'many': True
            }
        ),
        'organizations': (
            'outpost.django.campusonline.serializers.OrganizationSerializer',
            {
                'source': 'organizations',
                'many': True
            }
        ),
    }

    class Meta(PersonSerializer.Meta):
        exclude = (
            'username',
            'avatar_private',
            'hash',
        )

    def get_avatar(self, obj):
        if not obj.avatar_private:
            return None
        path = reverse(
            'campusonline:avatar-private',
            kwargs={
                'hash': obj.hash
            }
        )
        request = self.context.get('request')
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


class DistributionListSerializer(FlexFieldsModelSerializer):
    '''
    ## Expansions

    To activate relation expansion add the desired fields as a comma separated
    list to the `expand` query parameter like this:

        ?expand=<field>,<field>,<field>,...

    The following relational fields can be expanded:

     * `persons`

    '''
    @property
    def expandable_fields(self):
        serializer = 'PersonSerializer'
        request = self.context.get('request', None)
        if request:
            if request.user:
                if request.user.is_authenticated():
                    serializer = 'AuthenticatedPersonSerializer'
        return {
            'persons': (
                f'outpost.django.campusonline.serializers.{serializer}',
                {
                    'source': 'persons',
                    'many': True
                }
            ),
        }

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
    course = CourseSerializer()

    class Meta:
        model = models.Event
        fields = '__all__'


class BulletinSerializer(ModelSerializer):

    class Meta:
        model = models.Bulletin
        fields = '__all__'
