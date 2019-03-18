from django.urls import reverse
from drf_haystack.serializers import HaystackSerializerMixin
from phonenumbers import (
    PhoneNumberFormat,
    format_number,
)
from phonenumbers import parse as parse_number
from phonenumbers import phonenumberutil
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework.serializers import (
    ModelSerializer,
    PrimaryKeyRelatedField,
    SerializerMethodField,
)

from . import models
from .conf import settings


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
        fields = (
            'id',
            'category',
            'floor',
            'building',
            'title',
            'name_short',
            'name_full',
            'organization',
            'geo',
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
            'publication_authorship': (
                f'outpost.django.research.serializers.PublicationOrganizationSerializer',
                {
                    'source': 'publication_authorship',
                    'many': True
                }
            ),
        }

    class Meta:
        model = models.Organization
        fields = (
            'id',
            'name',
            'short',
            'sib_order',
            'category',
            'address',
            'email',
            'phone',
            'url',
            'parent',
            'persons',
            'publication_authorship',
        )


class PersonSerializer(FlexFieldsModelSerializer):
    '''
    ## Expansions

    To activate relation expansion add the desired fields as a comma separated
    list to the `expand` query parameter like this:

        ?expand=<field>,<field>,<field>,...

    The following relational fields can be expanded:

     * `functions` <i class="glyphicon glyphicon-lock"></i>
     * `organizations` <i class="glyphicon glyphicon-lock"></i>
     * `classification`
     * `expertise`
     * `knowledge`
     * `education`

    '''
    room = RoomSerializer()

    expandable_fields = {
        'classifications': (
            'outpost.django.research.serializers.ClassificationSerializer',
            {
                'source': 'classifications',
                'many': True
            }
        ),
        'expertise': (
            'outpost.django.research.serializers.ExpertiseSerializer',
            {
                'source': 'expertise',
                'many': True
            }
        ),
        'knowledge': (
            'outpost.django.research.serializers.KnowledgeSerializer',
            {
                'source': 'knowledge',
                'many': True
            }
        ),
        'education': (
            'outpost.django.research.serializers.EducationSerializer',
            {
                'source': 'education',
                'many': True
            }
        ),
    }

    class Meta:
        model = models.Person
        fields = (
            'id',
            'room',
            'avatar',
            'first_name',
            'last_name',
            'title',
            'consultation',
            'appendix',
            'phone',
            'classifications',
            'expertise',
            'knowledge',
            'education',
        )


class AuthenticatedPersonSerializer(PersonSerializer):
    avatar = SerializerMethodField()
    mobile = SerializerMethodField()

    @property
    def expandable_fields(self):
        base = 'outpost.django.campusonline.serializers'
        return {
            **super().expandable_fields,
            **{
                'functions': (
                    f'{base}.FunctionSerializer',
                    {
                        'source': 'functions',
                        'many': True
                    }
                ),
                'organizations': (
                    f'{base}.OrganizationSerializer',
                    {
                        'source': 'organizations',
                        'many': True
                    }
                ),
            }
        }

    class Meta(PersonSerializer.Meta):
        fields = PersonSerializer.Meta.fields + (
            'email',
            'sex',
            'mobile',
            'functions',
            'organizations',
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

    def get_mobile(self, obj):
        try:
            p = parse_number(
                obj.mobile,
                settings.CAMPUSONLINE_PHONE_NUMBER_REGION
            )
            return format_number(p, PhoneNumberFormat.INTERNATIONAL)
        except phonenumberutil.NumberParseException:
            return None


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


class StudentSerializer(ModelSerializer):

    class Meta:
        model = models.Student
        fields = (
            'first_name',
            'last_name',
            'title',
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
    course = CourseSerializer()

    class Meta:
        model = models.Event
        fields = '__all__'


class BulletinSerializer(ModelSerializer):

    class Meta:
        model = models.Bulletin
        fields = '__all__'


class BulletinPageSerializer(ModelSerializer):
    bulletin = BulletinSerializer()

    class Meta:
        model = models.BulletinPage
        fields = (
            'bulletin',
            'index',
            'text',
        )


class BulletinPageSearchSerializer(HaystackSerializerMixin, BulletinPageSerializer):

    class Meta(BulletinPageSerializer.Meta):
        search_fields = (
            'text',
        )
