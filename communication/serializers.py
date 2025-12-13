from rest_framework import serializers
from .models import ContactMessage, Testimonial, Statistics, News, Event, CampusLife
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

class StatisticSerializer(serializers.ModelSerializer):
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