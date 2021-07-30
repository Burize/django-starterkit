from rest_framework import serializers


class SignUpPayloadSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()
    email=serializers.EmailField()
