from rest_framework import serializers
from .models import CustomUser, StudentProfile, TutorProfile, StaffProfile, AlumniProfile


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
        model = StaffProfile
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
