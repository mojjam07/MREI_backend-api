# users/views.py
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import CustomUser, StudentProfile, TutorProfile, StaffProfile, AlumniProfile
from .serializers import UserSerializer, StudentProfileSerializer, TutorProfileSerializer, StaffProfileSerializer, AlumniProfileSerializer
from academics.models import Course


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


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def stats(request):
    active_students = CustomUser.objects.filter(role='student').count()
    courses = Course.objects.count()
    tutors = CustomUser.objects.filter(role='tutor').count()
    # Success rate: hardcoded for now, could be calculated from enrollments
    success_rate = 95
    return Response({
        'active_students': active_students,
        'courses': courses,
        'tutors': tutors,
        'success_rate': success_rate
    })
