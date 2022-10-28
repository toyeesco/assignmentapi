from rest_framework import serializers
from .models import User
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class UserCreationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=25)
    email = serializers.EmailField(max_length=80)
    password = serializers.CharField(min_length=5, write_only=True)
    address = serializers.CharField(max_length=100)
    city = serializers.CharField(max_length=50)
    phone_number = PhoneNumberField(allow_null=False, allow_blank=False)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj.email)
        return {
            'access': user.tokens()['access'],
            'refresh': user.tokens()['refresh']
        }

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'profile_pic', 'phone_number', 'tokens', 'city', 'address', 'location']

    def validate(self, attrs):
        username_exists = User.objects.filter(username=attrs['username']).exists()

        if username_exists:
            raise serializers.ValidationError(detail="User with username exists")

        email_exists = User.objects.filter(username=attrs['email']).exists()
        if email_exists:
            raise serializers.ValidationError(detail="User with email exists")

        phonenumber_exists = User.objects.filter(username=attrs['phone_number']).exists()
        if phonenumber_exists:
            raise serializers.ValidationError(detail="User with phonenumber exists")


        return super().validate(attrs)


    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            address=validated_data['address'],
            city=validated_data['city'],
            location=validated_data['location']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class ProfileSerializer(serializers.ModelSerializer):
    address = serializers.CharField(max_length=100)
    city = serializers.CharField(max_length=50)
    phone_number = PhoneNumberField(allow_null=False, allow_blank=False)

    class Meta:
        model = User
        fields = ['address', 'city', 'phone_number', 'profile_pic']

class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['city', 'location']

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'profile_pic', 'phone_number', 'tokens', 'city', 'address', 'location']