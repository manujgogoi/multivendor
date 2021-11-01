from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.HyperlinkedModelSerializer):

    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Please enter a strong password',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    class Meta:
        model = User
        fields = ['id', 'url', 'email', 'password', 'snippets']
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