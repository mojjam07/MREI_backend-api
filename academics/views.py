# academics/views.py
from rest_framework import viewsets, permissions, filters
from .models import Course, Enrollment, Assignment, Submission, Attendance
from .serializers import CourseSerializer, EnrollmentSerializer, AssignmentSerializer, SubmissionSerializer, AttendanceSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.select_related('tutor').all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['code', 'title', 'description']


class EnrollmentViewSet(viewsets.ModelViewSet):
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return Enrollment.objects.filter(student=user)
        return Enrollment.objects.all()


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]


class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.select_related('assignment', 'student').all()
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]