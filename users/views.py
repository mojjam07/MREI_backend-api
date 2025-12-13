
# users/views.py

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import CustomUser, StudentProfile, TutorProfile, AdminProfile, AlumniProfile
from .serializers import UserSerializer, StudentProfileSerializer, TutorProfileSerializer, StaffProfileSerializer, AlumniProfileSerializer, UserRegistrationSerializer
from academics.models import Course
from rest_framework_simplejwt.views import TokenObtainPairView


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'admin'


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            # Get the user from the token
            token = response.data.get('access')
            if token:
                from rest_framework_simplejwt.tokens import AccessToken
                access_token = AccessToken(token)
                user = CustomUser.objects.get(id=access_token['user_id'])
                user_data = UserSerializer(user).data
                # Make sure role is explicitly included in the response
                user_data['role'] = user.role
                response.data['user'] = user_data
        return response


# Add a view to get the current user
class CurrentUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        user_data = UserSerializer(user).data
        # Make sure role is explicitly included
        user_data['role'] = user.role
        return Response(user_data)


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



class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Create profile based on role
            if user.role == 'student':
                StudentProfile.objects.create(
                    user=user,
                    student_number=f"STU{user.id:06d}",  # Auto-generate student number
                    course_of_study="",  # Can be updated later
                    admission_year=2024  # Can be updated later
                )
            elif user.role == 'tutor':
                TutorProfile.objects.create(
                    user=user,
                    staff_number=f"TUT{user.id:06d}",  # Auto-generate staff number
                    department="",  # Can be updated later
                    bio="",  # Can be updated later
                    subjects=""  # Can be updated later
                )
            elif user.role == 'admin':
                AdminProfile.objects.create(
                    user=user,
                    role_title="",  # Can be updated later
                    department=""  # Can be updated later
                )
            elif user.role == 'alumni':
                AlumniProfile.objects.create(
                    user=user,
                    graduation_year=2024,  # Can be updated later
                    current_employer="",  # Can be updated later
                    bio=""  # Can be updated later
                )
            
            return Response({
                'message': 'User created successfully',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'role': user.role
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
