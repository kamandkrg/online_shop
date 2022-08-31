from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


User = get_user_model()


class CreateUserSerializers(serializers.ModelSerializer):
    password1 = serializers.CharField(label='Password', write_only=True)
    password2 = serializers.CharField(label='Password confirmation', write_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'username',
                  'age', 'sex', 'password1', 'password2')

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise ValidationError('password is not mach')
        return attrs

    def save(self, **kwargs):

        validated_data = {**self.validated_data, **kwargs}
        password = validated_data.pop('password1')
        password2 = validated_data.pop('password2')
        user = User.objects.create_user(
            **validated_data
        )
        user.set_password(password)
        user.save()
        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(label='new Password', write_only=True)
    password2 = serializers.CharField(label='Password confirmation', write_only=True)
    old_password = serializers.CharField(label='Old Password', write_only=True, allow_blank=True)

    class Meta:
        model = User
        fields = ('password1', 'password2', 'old_password')

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise ValidationError('password is not mach')
        return attrs

    def validate_old_password(self, attr):
        user = self.context['request'].user
        if user.is_staff or user.is_superuser:
            return True
        if not user.check_password(attr):
            raise ValidationError('old password is not correct')
        return True

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password1'])
        instance.save()
        return instance


class UpdateDestroyRetrieveUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(label='Password', write_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'username',
                  'age', 'sex', 'password')

    def validate_password(self, attr):
        user = self.context['request'].user
        if not user.check_password(attr):
            raise ValidationError('password is not correct')
        return True

    def update(self, instance, validated_data):
        validated_data.pop('password')
        for key in validated_data:
            setattr(instance, key, validated_data[key])
        instance.save()
        return instance
