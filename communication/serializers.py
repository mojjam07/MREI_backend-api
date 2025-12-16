
from rest_framework import serializers
from .models import ContactMessage, Testimonial, Statistics, News, Event, CampusLife, Message, Notification, Announcement, Book
from users.serializers import UserSerializer

# -------------------------------------
# Messages
# -------------------------------------


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = "__all__"

# --------------------------------------
# Testimonials
# --------------------------------------

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = "__all__"

# --------------------------------------
# Statistics
# --------------------------------------

class StatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistics
        fields = '__all__'

# --------------------------------------
# News
# --------------------------------------

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'

# --------------------------------------
# Event
# --------------------------------------

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


# --------------------------------------
# CampusLife
# --------------------------------------

class CampusLifeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampusLife
        field = '__all__'

# --------------------------------------
# Message
# --------------------------------------

class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)
    receiver_username = serializers.CharField(source='receiver.username', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)
    assignment_title = serializers.CharField(source='assignment.title', read_only=True)
    
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['sent_at', 'is_read', 'read_at']

# --------------------------------------
# Notification
# --------------------------------------

class NotificationSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)
    assignment_title = serializers.CharField(source='assignment.title', read_only=True)
    
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ['created_at', 'is_read', 'read_at']

# --------------------------------------
# Announcement
# --------------------------------------

class AnnouncementSerializer(serializers.ModelSerializer):
    admin_username = serializers.CharField(source='admin.username', read_only=True)

    class Meta:
        model = Announcement
        fields = '__all__'
        read_only_fields = ['created_at']


class BookSerializer(serializers.ModelSerializer):
    uploaded_by_name = serializers.CharField(source='uploaded_by.get_full_name', read_only=True)
    cover_image_url = serializers.CharField(source='get_cover_image', read_only=True)
    pdf_file_url = serializers.CharField(source='get_pdf_file', read_only=True)

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'description', 'cover_image', 'cover_image_url',
            'pdf_file', 'pdf_file_url', 'isbn', 'genre', 'publication_year',
            'language', 'pages', 'is_available', 'uploaded_by', 'uploaded_by_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['uploaded_by', 'created_at', 'updated_at']
