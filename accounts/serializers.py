from django.contrib.auth import get_user_model
from rest_framework import serializers
from vendor.models import Vendor

User = get_user_model()

class UserSerializer(serializers.HyperlinkedModelSerializer):

    vendor = serializers.HyperlinkedRelatedField(view_name='vendor-detail', read_only=True, many=False)

    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    class Meta:
        model = User
        fields = ['id', 'url', 'email', 'password', 'vendor']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = User.objects.create(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class PasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, data):
        old_pass = data.get('old_password')
        new_pass = data.get('new_password')
        if old_pass == new_pass:
            raise serializers.ValidationError("Please enter a new password!")
        return data

class EmailSerializer(serializers.Serializer):
    '''
    Serializer for email change endpoint.
    '''
    email = serializers.EmailField(max_length=255)

    def validate_email(self, value):
        '''
        Check is email already exist
        '''
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email already exists!")
        return value
