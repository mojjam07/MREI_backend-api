# users/views.py
from rest_framework import viewsets, permissions
from .models import CustomUser, StudentProfile, TutorProfile, StaffProfile, AlumniProfile
from .serializers import UserSerializer, StudentProfileSerializer, TutorProfileSerializer, StaffProfileSerializer, AlumniProfileSerializer


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'admin'


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_permissions(self):
        if self.action in ['list', 'destroy', 'create']:
            return [permissions.IsAuthenticated(), IsAdminOrReadOnly()]
        return super().get_permissions()


class StudentProfileViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.select_related('user').all()
    serializer_class = StudentProfileSerializer
    permission_classes = [permissions.IsAuthenticated]