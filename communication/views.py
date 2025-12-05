# communication/views.py
from rest_framework import viewsets, permissions
from .models import Announcement, Notification
from .serializers import AnnouncementSerializer, NotificationSerializer


class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)