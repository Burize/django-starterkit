from rest_framework import serializers


class LoginPayloadSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()
