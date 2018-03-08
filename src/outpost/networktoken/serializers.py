from rest_framework import serializers

from . import models


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Token
        fields = (
            'id',
            'value',
            'expires',
        )
