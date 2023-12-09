import re
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from phonenumber_field.serializerfields import PhoneNumberField
from django.contrib.humanize.templatetags import humanize
from .models import Role



User = get_user_model()
#<------------------------------------------------------------User-Side-Start-------------------------------------------------------->
class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    phone_number = serializers.CharField(
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all(), message="Phone number already exists."),
        ]
    )
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True) 

    class Meta:
        model = User
        fields = ['email', 'phone_number', 'password', 'password2'] 

    def validate_password(self, password):
        # Password policy: Minimum 6 characters, at least one uppercase letter, one lowercase letter, and one digit
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{6,}$', password):
            raise serializers.ValidationError(
                "Password must be at least 6 characters long and contain at least one uppercase letter, one lowercase letter, and one digit."
            )
        return password

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        phone_number = attrs.get('phone_number', None)
        if phone_number:
            # Define a regex pattern for a standard phone number format (adjust as needed)
            phone_number_pattern = r'^\+\d{1,3}-\d{3,14}$'

            # Check if the phone number matches the pattern
            if not re.match(phone_number_pattern, phone_number):
                raise serializers.ValidationError({"phone_number": "Invalid phone number format."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            phone_number=validated_data['phone_number']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role 
        token['email'] = user.email
        token['type'] = user.subscription_plan 
        return token

class CustomTokenRefreshSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['access'] = str(refresh.access_token)
        data['role'] = self.user.role
        data['subscription_plan'] = self.user.subscription_plan 
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'city', 'state', 'country', 'qualification', 'skills', 'subjects', 'category']
#<------------------------------------------------------------------User-Side-End--------------------------------------------------->



#<------------------------------------------------------------------Admin-side-Start------------------------------------------------>



class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    last_login_display = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'phone_number', 'first_name', 'last_name', 'is_active', 'display_pic', 'role', 'date_joined', 'last_login_display']
    def get_last_login_display(self, obj):
        return humanize.naturaltime(obj.last_login)


#<------------------------------------------------------------------Admin-Side-End--------------------------------------------------->



#<------------------------------------------------------------------Tutor-Side-Start------------------------------------------------->


class TutorRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    phone_number = serializers.CharField(
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all(), message="Phone number already exists."),
        ]
    )
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)  # Add password2 field

    class Meta:
        model = User
        fields = ['email', 'phone_number', 'password', 'password2']  # Include password2 field in fields

    def validate_password(self, password):
        # Password policy: Minimum 6 characters, at least one uppercase letter, one lowercase letter, and one digit
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{6,}$', password):
            raise serializers.ValidationError(
                "Password must be at least 6 characters long and contain at least one uppercase letter, one lowercase letter, and one digit."
            )
        return password

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        phone_number = attrs.get('phone_number', None)
        if phone_number:
            # Define a regex pattern for a standard phone number format (adjust as needed)
            phone_number_pattern = r'^\+\d{1,3}-\d{3,14}$'

            # Check if the phone number matches the pattern
            if not re.match(phone_number_pattern, phone_number):
                raise serializers.ValidationError({"phone_number": "Invalid phone number format."})
        return attrs
    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            is_tutor = True ,
            role = Role.TUTOR
        )

        user.set_password(validated_data['password'])
         # Mark the user as a tutor
        user.save()
        print(user.email,1111111111111111111111111)
        print(user.is_tutor)
        return user
