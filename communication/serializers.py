from rest_framework import serializers
from .models import Announcement, Notification
from users.serializers import UserSerializer


# -------------------------------------
# Announcement Serializer
# -------------------------------------
class AnnouncementSerializer(serializers.ModelSerializer):
    """
    Serializer for the Announcement model.
    """

    class Meta:
        model = Announcement
        fields = [
            "id",
            "title",
            "content",
            "visible_to",
            "start_date",
            "end_date",
        ]
        read_only_fields = ["id"]


# -------------------------------------
# Notification Serializer
# -------------------------------------
class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Notification model.
    """

    user = UserSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = [
            "id",
            "user",
            "title",
            "message",
            "type",
            "read",
            "created_at",
        ]
        read_only_fields = ["id", "user", "created_at"]