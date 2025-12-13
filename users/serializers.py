from rest_framework import serializers
from .models import CustomUser, StudentProfile, TutorProfile, AdminProfile, AlumniProfile


# -------------------------------------
# User Serializer
# -------------------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "preferred_language",
            "profile_image",
        ]
        read_only_fields = ["id", "role"]


# -------------------------------------
# Student Profile Serializer
# -------------------------------------
class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = StudentProfile
        fields = "__all__"
        read_only_fields = ["id", "user"]


# -------------------------------------
# Tutor Profile Serializer
# -------------------------------------
class TutorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = TutorProfile
        fields = "__all__"
        read_only_fields = ["id", "user"]


# -------------------------------------
# Staff Profile Serializer
# -------------------------------------
class StaffProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = AdminProfile
        fields = "__all__"
        read_only_fields = ["id", "user"]



# -------------------------------------
# Alumni Profile Serializer
# -------------------------------------
class AlumniProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = AlumniProfile
        fields = "__all__"
        read_only_fields = ["id", "user"]


# -------------------------------------
# User Registration Serializer
# -------------------------------------
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "email",
            "password",
            "password_confirm",
            "first_name",
            "last_name",
            "role"
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match.")
        return attrs

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        # Auto-generate username from email
        validated_data['username'] = validated_data['email']
        user = CustomUser.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user
