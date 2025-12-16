
from rest_framework import serializers
from .models import (
    Course, Enrollment, Assignment, AssignmentSubmission, Attendance,
    AdminTutorAssignment, AdminStudentAssignment, ClassSchedule, TutorPerformance
)
from users.models import CustomUser


class CourseSerializer(serializers.ModelSerializer):
    tutor_name = serializers.CharField(source='tutor.username', read_only=True)
    enrollment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]
    
    def get_enrollment_count(self, obj):
        return obj.enrollments.filter(status='enrolled').count()


class EnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.username', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)
    course_code = serializers.CharField(source='course.code', read_only=True)
    
    class Meta:
        model = Enrollment
        fields = "__all__"
        read_only_fields = ["id", "enrolled_at"]


class AssignmentSerializer(serializers.ModelSerializer):
    tutor_name = serializers.CharField(source='tutor.username', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)
    submission_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Assignment
        fields = "__all__"
        read_only_fields = ["id", "created_at"]
    
    def get_submission_count(self, obj):
        return obj.submissions.count()


class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.username', read_only=True)
    assignment_title = serializers.CharField(source='assignment.title', read_only=True)
    graded_by_name = serializers.CharField(source='graded_by.username', read_only=True)
    
    class Meta:
        model = AssignmentSubmission
        fields = "__all__"
        read_only_fields = ["id", "submitted_at", "graded_at"]
    
    def validate(self, data):
        # Only tutors can grade submissions
        if self.context['request'].user.role != 'tutor':
            raise serializers.ValidationError("Only tutors can grade assignments.")
        return data


class AdminTutorAssignmentSerializer(serializers.ModelSerializer):
    admin_name = serializers.CharField(source='admin.username', read_only=True)
    tutor_name = serializers.CharField(source='tutor.username', read_only=True)
    
    class Meta:
        model = AdminTutorAssignment
        fields = "__all__"
        read_only_fields = ["id", "assigned_date"]


class AdminStudentAssignmentSerializer(serializers.ModelSerializer):
    admin_name = serializers.CharField(source='admin.username', read_only=True)
    student_name = serializers.CharField(source='student.username', read_only=True)
    
    class Meta:
        model = AdminStudentAssignment
        fields = "__all__"
        read_only_fields = ["id", "assigned_date"]


class ClassScheduleSerializer(serializers.ModelSerializer):
    tutor_name = serializers.CharField(source='tutor.username', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)
    attendance_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ClassSchedule
        fields = "__all__"
        read_only_fields = ["id", "created_at"]
    
    def get_attendance_count(self, obj):
        return obj.attendances.filter(status='present').count()


class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.username', read_only=True)
    class_title = serializers.CharField(source='class_schedule.title', read_only=True)
    
    class Meta:
        model = Attendance
        fields = "__all__"
        read_only_fields = ["id", "attended_at"]


class TutorPerformanceSerializer(serializers.ModelSerializer):
    tutor_name = serializers.CharField(source='tutor.username', read_only=True)
    
    class Meta:
        model = TutorPerformance
        fields = "__all__"
        read_only_fields = ["id", "created_at"]


# Dashboard Analytics Serializers
class TutorDashboardSerializer(serializers.Serializer):
    """Serializer for tutor dashboard data"""
    courses_taught = serializers.IntegerField()
    total_students = serializers.IntegerField()
    pending_grading = serializers.IntegerField()
    upcoming_classes = serializers.IntegerField()
    avg_rating = serializers.DecimalField(max_digits=3, decimal_places=2)
    attendance_rate = serializers.DecimalField(max_digits=5, decimal_places=2)


class StudentDashboardSerializer(serializers.Serializer):
    """Serializer for student dashboard data"""
    enrolled_courses = serializers.IntegerField()
    completed_courses = serializers.IntegerField()
    pending_assignments = serializers.IntegerField()
    overall_progress = serializers.DecimalField(max_digits=5, decimal_places=2)
    avg_grade = serializers.DecimalField(max_digits=6, decimal_places=2)
    attendance_rate = serializers.DecimalField(max_digits=5, decimal_places=2)


class AdminDashboardSerializer(serializers.Serializer):
    """Serializer for admin dashboard data"""
    total_users = serializers.IntegerField()
    total_students = serializers.IntegerField()
    total_tutors = serializers.IntegerField()
    total_courses = serializers.IntegerField()
    active_enrollments = serializers.IntegerField()
    completion_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    system_health = serializers.DictField()


# Detailed serializers with nested relationships
class DetailedCourseSerializer(serializers.ModelSerializer):
    tutor = serializers.StringRelatedField()
    enrollments = EnrollmentSerializer(many=True, read_only=True)
    assignments = AssignmentSerializer(many=True, read_only=True)
    class_schedules = ClassScheduleSerializer(many=True, read_only=True)
    
    class Meta:
        model = Course
        fields = "__all__"


class DetailedAssignmentSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField()
    tutor = serializers.StringRelatedField()
    submissions = AssignmentSubmissionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Assignment
        fields = "__all__"


class DetailedEnrollmentSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField()
    course = serializers.StringRelatedField()
    attendance_records = AttendanceSerializer(many=True, read_only=True)
    
    class Meta:
        model = Enrollment
        fields = "__all__"
