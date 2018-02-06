from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from . import models


class ContentTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContentType
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Notification
        fields = '__all__'


class TaskSerializer(serializers.BaseSerializer):
    id = serializers.CharField(max_length=256)
    state = serializers.CharField(max_length=256)
    info = serializers.DictField()

    def to_representation(self, obj):
        return {
            'id': obj.id,
            'state': obj.state,
            'info': obj.info
        }
