from django.contrib.auth import get_user_model
from rest_framework import serializers


# serializer convert python objects to and from JSON object like for get=> Python object->JSON and post=> JSON->Python object
class UserSerializer(serializers.ModelSerializer):
    # the meta class tells django RF the models and fields and other arguments that we want to send to the serializer
    class Meta:
        model = get_user_model
        fields = ["email", "password", "name"]
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    # create method overrides the behavior that the serializer does when we create new objects out of serializer because we want the password to be save as encrypted and not directly.
    # the create method will be called after it passes validations mentioned in meta class and if fails it will give 400 status
    def create(self):
        return get_user_model().objects.create_user(**validated_data)
