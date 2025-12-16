
# academics/views.py
from rest_framework import viewsets, permissions, filters, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Count, Avg, Q, F
from django.db.models.functions import TruncDate
from .models import (
    Course, Enrollment, Assignment, AssignmentSubmission, Attendance,
    AdminTutorAssignment, AdminStudentAssignment, ClassSchedule, TutorPerformance
)
from .serializers import (
    CourseSerializer, EnrollmentSerializer, AssignmentSerializer, AssignmentSubmissionSerializer,
    AttendanceSerializer, AdminTutorAssignmentSerializer, AdminStudentAssignmentSerializer,
    ClassScheduleSerializer, TutorPerformanceSerializer,
    TutorDashboardSerializer, StudentDashboardSerializer, AdminDashboardSerializer,
    DetailedCourseSerializer, DetailedAssignmentSerializer, DetailedEnrollmentSerializer
)
from users.permissions import (
    IsTutor, IsStudent, IsAdmin, RoleBasedPermission, IsOwnerOrAdmin,
    IsTutorOfStudent, IsEnrolledInCourse, IsAdminOfUser
)
from users.models import CustomUser


# -------------------------------------
# Enhanced Course ViewSet
# -------------------------------------
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.select_related('tutor').all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated, RoleBasedPermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ['code', 'title', 'description', 'subject']
    required_roles = ['admin', 'tutor', 'student']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            # Students see only courses they're enrolled in or all active courses
            return Course.objects.filter(
                Q(enrollments__student=user) | Q(is_active=True)
            ).select_related('tutor').distinct()
        elif user.role == 'tutor':
            # Tutors see only their own courses
            return Course.objects.filter(tutor=user).select_related('tutor')
        elif user.role == 'admin':
            # Admins see all courses
            return Course.objects.select_related('tutor').all()
        return Course.objects.none()

    @action(detail=True, methods=['get'])
    def enrollments(self, request, pk=None):
        """Get enrollments for a specific course"""
        course = self.get_object()
        enrollments = course.enrollments.all()
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def assignments(self, request, pk=None):
        """Get assignments for a specific course"""
        course = self.get_object()
        assignments = course.assignments.all()
        serializer = AssignmentSerializer(assignments, many=True)
        return Response(serializer.data)


# -------------------------------------
# Enhanced Enrollment ViewSet
# -------------------------------------
class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.select_related('student', 'course').all()
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated, RoleBasedPermission]
    required_roles = ['admin', 'tutor', 'student']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return Enrollment.objects.filter(student=user).select_related('student', 'course')
        elif user.role == 'tutor':
            # Tutors see enrollments for their courses
            return Enrollment.objects.filter(course__tutor=user).select_related('student', 'course')
        elif user.role == 'admin':
            return Enrollment.objects.select_related('student', 'course').all()
        return Enrollment.objects.none()

    @action(detail=False, methods=['post'])
    def enroll_student(self, request):
        """Enroll a student in a course"""
        course_id = request.data.get('course_id')
        student_id = request.data.get('student_id')
        
        # Check if student is trying to enroll themselves or admin is enrolling someone
        if request.user.role == 'student' and request.user.id != student_id:
            return Response(
                {'error': 'Students can only enroll themselves'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            course = Course.objects.get(id=course_id)
            student = CustomUser.objects.get(id=student_id, role='student')
            
            enrollment, created = Enrollment.objects.get_or_create(
                student=student,
                course=course
            )
            
            if created:
                serializer = EnrollmentSerializer(enrollment)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {'error': 'Student is already enrolled in this course'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except (Course.DoesNotExist, CustomUser.DoesNotExist) as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )


# -------------------------------------
# Enhanced Assignment ViewSet
# -------------------------------------
class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.select_related('course', 'tutor').all()
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated, RoleBasedPermission]
    required_roles = ['admin', 'tutor', 'student']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            # Students see assignments for courses they're enrolled in
            return Assignment.objects.filter(
                course__enrollments__student=user
            ).select_related('course', 'tutor')
        elif user.role == 'tutor':
            # Tutors see only their own assignments
            return Assignment.objects.filter(tutor=user).select_related('course', 'tutor')
        elif user.role == 'admin':
            return Assignment.objects.select_related('course', 'tutor').all()
        return Assignment.objects.none()

    @action(detail=True, methods=['get'])
    def submissions(self, request, pk=None):
        """Get submissions for a specific assignment"""
        assignment = self.get_object()
        submissions = assignment.submissions.all()
        serializer = AssignmentSubmissionSerializer(submissions, many=True)
        return Response(serializer.data)


# -------------------------------------
# Assignment Submission ViewSet
# -------------------------------------
class AssignmentSubmissionViewSet(viewsets.ModelViewSet):
    queryset = AssignmentSubmission.objects.select_related('assignment', 'student', 'graded_by').all()
    serializer_class = AssignmentSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated, RoleBasedPermission, IsOwnerOrAdmin]
    required_roles = ['admin', 'tutor', 'student']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            # Students see only their own submissions
            return AssignmentSubmission.objects.filter(student=user).select_related('assignment', 'student', 'graded_by')
        elif user.role == 'tutor':
            # Tutors see submissions for their assignments
            return AssignmentSubmission.objects.filter(
                assignment__tutor=user
            ).select_related('assignment', 'student', 'graded_by')
        elif user.role == 'admin':
            return AssignmentSubmission.objects.select_related('assignment', 'student', 'graded_by').all()
        return AssignmentSubmission.objects.none()

    def perform_create(self, serializer):
        """Create submission for students"""
        serializer.save(student=self.request.user)

    @action(detail=True, methods=['post'])
    def grade(self, request, pk=None):
        """Grade a submission (tutors only)"""
        if request.user.role != 'tutor':
            return Response(
                {'error': 'Only tutors can grade assignments'},
                status=status.HTTP_403_FORBIDDEN
            )

        submission = self.get_object()
        grade = request.data.get('grade')
        feedback = request.data.get('feedback', '')

        if grade is not None:
            submission.grade = grade
            submission.feedback = feedback
            submission.graded_by = request.user
            submission.graded_at = timezone.now()
            submission.status = 'graded'
            submission.save()

            serializer = AssignmentSubmissionSerializer(submission)
            return Response(serializer.data)
        else:
            return Response(
                {'error': 'Grade is required'},
                status=status.HTTP_400_BAD_REQUEST
            )


# -------------------------------------
# Class Schedule ViewSet
# -------------------------------------
class ClassScheduleViewSet(viewsets.ModelViewSet):
    queryset = ClassSchedule.objects.select_related('course', 'tutor').all()
    serializer_class = ClassScheduleSerializer
    permission_classes = [permissions.IsAuthenticated, RoleBasedPermission]
    required_roles = ['admin', 'tutor', 'student']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            # Students see schedules for their enrolled courses
            return ClassSchedule.objects.filter(
                course__enrollments__student=user
            ).select_related('course', 'tutor')
        elif user.role == 'tutor':
            # Tutors see only their own class schedules
            return ClassSchedule.objects.filter(tutor=user).select_related('course', 'tutor')
        elif user.role == 'admin':
            return ClassSchedule.objects.select_related('course', 'tutor').all()
        return ClassSchedule.objects.none()


# -------------------------------------
# Attendance ViewSet
# -------------------------------------
class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.select_related('class_schedule', 'student').all()
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated, RoleBasedPermission]
    required_roles = ['admin', 'tutor', 'student']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            # Students see only their own attendance
            return Attendance.objects.filter(student=user).select_related('class_schedule', 'student')
        elif user.role == 'tutor':
            # Tutors see attendance for their classes
            return Attendance.objects.filter(
                class_schedule__tutor=user
            ).select_related('class_schedule', 'student')
        elif user.role == 'admin':
            return Attendance.objects.select_related('class_schedule', 'student').all()
        return Attendance.objects.none()


# -------------------------------------
# Admin Management Views
# -------------------------------------
class AdminTutorManagementView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    
    def get(self, request):
        """Get all tutors with performance metrics"""
        tutors = CustomUser.objects.filter(role='tutor').select_related('tutor_profile')
        
        tutor_data = []
        for tutor in tutors:
            courses_taught = Course.objects.filter(tutor=tutor).count()
            students_managed = Enrollment.objects.filter(course__tutor=tutor, status='enrolled').count()
            
            # Calculate performance metrics
            avg_rating = TutorPerformance.objects.filter(tutor=tutor).aggregate(
                avg_rating=Avg('avg_rating')
            )['avg_rating'] or 0
            
            attendance_rate = TutorPerformance.objects.filter(tutor=tutor).aggregate(
                attendance_rate=Avg('attendance_rate')
            )['attendance_rate'] or 0
            
            tutor_data.append({
                'id': tutor.id,
                'username': tutor.username,
                'email': tutor.email,
                'department': tutor.tutor_profile.department if hasattr(tutor, 'tutor_profile') else 'N/A',
                'subjects': tutor.tutor_profile.subjects if hasattr(tutor, 'tutor_profile') else 'N/A',
                'courses_taught': courses_taught,
                'students_managed': students_managed,
                'avg_rating': float(avg_rating),
                'attendance_rate': float(attendance_rate),
                'status': 'active'  # Could be dynamic based on assignments
            })
        
        return Response(tutor_data)


class AdminStudentManagementView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    
    def get(self, request):
        """Get all students with progress metrics"""
        students = CustomUser.objects.filter(role='student').select_related('student_profile')
        
        student_data = []
        for student in students:
            enrollments = Enrollment.objects.filter(student=student)
            courses_enrolled = enrollments.count()
            completed_courses = enrollments.filter(status='completed').count()
            progress_rate = (completed_courses / courses_enrolled * 100) if courses_enrolled > 0 else 0
            
            recent_submissions = AssignmentSubmission.objects.filter(
                student=student,
                submitted_at__gte=timezone.now() - timezone.timedelta(days=30)
            ).count()
            
            student_data.append({
                'id': student.id,
                'username': student.username,
                'email': student.email,
                'student_number': student.student_profile.student_number if hasattr(student, 'student_profile') else 'N/A',
                'course_of_study': student.student_profile.course_of_study if hasattr(student, 'student_profile') else 'N/A',
                'admission_year': student.student_profile.admission_year if hasattr(student, 'student_profile') else 'N/A',
                'courses_enrolled': courses_enrolled,
                'completed_courses': completed_courses,
                'progress_rate': float(progress_rate),
                'recent_submissions': recent_submissions,
                'status': student.student_profile.status if hasattr(student, 'student_profile') else 'active'
            })
        
        return Response(student_data)


# -------------------------------------
# Dashboard Analytics Views
# -------------------------------------
class TutorDashboardView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, IsTutor]
    serializer_class = TutorDashboardSerializer
    
    def get(self, request):
        """Get tutor dashboard analytics"""
        tutor = request.user
        
        courses_taught = Course.objects.filter(tutor=tutor).count()
        students_managed = Enrollment.objects.filter(course__tutor=tutor, status='enrolled').distinct().count()
        pending_grading = AssignmentSubmission.objects.filter(
            assignment__tutor=tutor,
            grade__isnull=True
        ).count()
        upcoming_classes = ClassSchedule.objects.filter(
            tutor=tutor,
            scheduled_date__gte=timezone.now()
        ).count()
        
        # Calculate performance metrics
        avg_rating = TutorPerformance.objects.filter(tutor=tutor).aggregate(
            avg_rating=Avg('avg_rating')
        )['avg_rating'] or 0
        
        attendance_rate = ClassSchedule.objects.filter(tutor=tutor).aggregate(
            attendance_rate=Avg('attendances__status')
        )['attendance_rate'] or 0
        
        data = {
            'courses_taught': courses_taught,
            'total_students': students_managed,
            'pending_grading': pending_grading,
            'upcoming_classes': upcoming_classes,
            'avg_rating': float(avg_rating),
            'attendance_rate': float(attendance_rate)
        }
        
        serializer = TutorDashboardSerializer(data)
        return Response(serializer.data)


class StudentDashboardView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, IsStudent]
    serializer_class = StudentDashboardSerializer
    
    def get(self, request):
        """Get student dashboard analytics"""
        student = request.user
        
        enrollments = Enrollment.objects.filter(student=student)
        enrolled_courses = enrollments.count()
        completed_courses = enrollments.filter(status='completed').count()
        
        # Calculate overall progress
        total_progress = sum([float(e.progress) for e in enrollments])
        overall_progress = total_progress / enrolled_courses if enrolled_courses > 0 else 0
        
        # Get pending assignments
        pending_assignments = AssignmentSubmission.objects.filter(
            student=student,
            grade__isnull=True
        ).count()
        
        # Calculate average grade
        graded_submissions = AssignmentSubmission.objects.filter(
            student=student,
            grade__isnull=False
        )
        avg_grade = graded_submissions.aggregate(avg_grade=Avg('grade'))['avg_grade'] or 0
        
        # Calculate attendance rate
        attendance_records = Attendance.objects.filter(student=student)
        total_classes = attendance_records.count()
        attended_classes = attendance_records.filter(status__in=['present', 'late']).count()
        attendance_rate = (attended_classes / total_classes * 100) if total_classes > 0 else 0
        
        data = {
            'enrolled_courses': enrolled_courses,
            'completed_courses': completed_courses,
            'pending_assignments': pending_assignments,
            'overall_progress': float(overall_progress),
            'avg_grade': float(avg_grade),
            'attendance_rate': float(attendance_rate)
        }
        
        serializer = StudentDashboardSerializer(data)
        return Response(serializer.data)


class AdminDashboardView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    serializer_class = AdminDashboardSerializer
    
    def get(self, request):
        """Get admin dashboard analytics"""
        total_users = CustomUser.objects.count()
        total_students = CustomUser.objects.filter(role='student').count()
        total_tutors = CustomUser.objects.filter(role='tutor').count()
        total_courses = Course.objects.count()
        active_enrollments = Enrollment.objects.filter(status='enrolled').count()
        
        # Calculate completion rate
        total_enrollments = Enrollment.objects.count()
        completed_enrollments = Enrollment.objects.filter(status='completed').count()
        completion_rate = (completed_enrollments / total_enrollments * 100) if total_enrollments > 0 else 0
        
        # System health metrics
        system_health = {
            'active_users_24h': CustomUser.objects.filter(
                last_login__gte=timezone.now() - timezone.timedelta(days=1)
            ).count(),
            'recent_registrations': CustomUser.objects.filter(
                date_joined__gte=timezone.now() - timezone.timedelta(days=7)
            ).count(),
            'pending_submissions': AssignmentSubmission.objects.filter(
                grade__isnull=True
            ).count()
        }
        
        data = {
            'total_users': total_users,
            'total_students': total_students,
            'total_tutors': total_tutors,
            'total_courses': total_courses,
            'active_enrollments': active_enrollments,
            'completion_rate': float(completion_rate),
            'system_health': system_health
        }
        
        serializer = AdminDashboardSerializer(data)
        return Response(serializer.data)
