
from django.db import models
from django.utils import timezone
from users.models import CustomUser, StudentProfile, TutorProfile


# -------------------------------------
# Enhanced Course Model
# -------------------------------------
class Course(models.Model):
    code = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    tutor = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, limit_choices_to={"role": "tutor"})
    credit_hours = models.IntegerField(default=3)
    subject = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    max_students = models.IntegerField(default=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.title}"


# -------------------------------------
# Enhanced Enrollment Model
# -------------------------------------
class Enrollment(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={"role": "student"})
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('enrolled', 'Enrolled'),
        ('completed', 'Completed'),
        ('dropped', 'Dropped'),
        ('suspended', 'Suspended')
    ], default='enrolled')
    grade = models.CharField(max_length=5, blank=True, null=True)
    progress = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    final_grade = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = ("student", "course")

    def __str__(self):
        return f"{self.student.username} -> {self.course.code}"


# -------------------------------------
# Enhanced Assignment Model
# -------------------------------------
class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    tutor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={"role": "tutor"})
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField()
    max_points = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assignment_type = models.CharField(max_length=20, choices=[
        ('essay', 'Essay'),
        ('quiz', 'Quiz'),
        ('project', 'Project'),
        ('presentation', 'Presentation'),
        ('homework', 'Homework')
    ], default='homework')
    attachment_url = models.URLField(blank=True, null=True)
    instructions = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


# -------------------------------------
# Enhanced Submission Model
# -------------------------------------
class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={"role": "student"})
    submitted_content = models.TextField()
    file_url = models.URLField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    grade = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(blank=True, null=True)
    graded_at = models.DateTimeField(null=True, blank=True)
    graded_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='grades_given', null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('submitted', 'Submitted'),
        ('graded', 'Graded'),
        ('late', 'Late'),
        ('missing', 'Missing')
    ], default='submitted')

    class Meta:
        unique_together = ('assignment', 'student')

    def __str__(self):
        return f"{self.assignment.title} -> {self.student.username}"

    @property
    def is_graded(self):
        return self.grade is not None

    @property
    def is_late(self):
        return self.status == 'late'


# -------------------------------------
# Admin-Tutor Assignment Model
# -------------------------------------
class AdminTutorAssignment(models.Model):
    admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='managed_tutors', limit_choices_to={"role": "admin"})
    tutor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='assigned_admin', limit_choices_to={"role": "tutor"})
    assigned_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('inactive', 'Inactive')
    ], default='active')
    notes = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('admin', 'tutor')


# -------------------------------------
# Admin-Student Assignment Model
# -------------------------------------
class AdminStudentAssignment(models.Model):
    admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='managed_students', limit_choices_to={"role": "admin"})
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='assigned_admin_student', limit_choices_to={"role": "student"})
    assigned_date = models.DateTimeField(auto_now_add=True)
    support_type = models.CharField(max_length=50, choices=[
        ('academic', 'Academic Support'),
        ('financial', 'Financial Support'),
        ('disciplinary', 'Disciplinary'),
        ('general', 'General Support')
    ])
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('resolved', 'Resolved'),
        ('pending', 'Pending')
    ], default='active')


# -------------------------------------
# Class Schedule Model
# -------------------------------------
class ClassSchedule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='class_schedules')
    tutor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='class_schedules', limit_choices_to={"role": "tutor"})
    title = models.CharField(max_length=255)
    description = models.TextField()
    scheduled_date = models.DateTimeField()
    duration_minutes = models.IntegerField(default=60)
    meeting_link = models.URLField(blank=True, null=True)
    attendance_tracking = models.BooleanField(default=True)
    class_type = models.CharField(max_length=20, choices=[
        ('lecture', 'Lecture'),
        ('tutorial', 'Tutorial'),
        ('lab', 'Lab'),
        ('exam', 'Exam'),
        ('presentation', 'Presentation')
    ], default='lecture')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.scheduled_date}"


# -------------------------------------
# Enhanced Attendance Model
# -------------------------------------
class Attendance(models.Model):
    class_schedule = models.ForeignKey(ClassSchedule, on_delete=models.CASCADE, related_name='attendances')
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='attendances', limit_choices_to={"role": "student"})
    attended_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('present', 'Present'),
        ('late', 'Late'),
        ('absent', 'Absent'),
        ('excused', 'Excused')
    ], default='present')
    notes = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('class_schedule', 'student')


# -------------------------------------
# Tutor Performance Metrics Model
# -------------------------------------
class TutorPerformance(models.Model):
    tutor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='performance_metrics', limit_choices_to={"role": "tutor"})
    period_start = models.DateTimeField()
    period_end = models.DateTimeField()
    courses_taught = models.IntegerField(default=0)
    students_managed = models.IntegerField(default=0)
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    attendance_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    assignment_completion_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tutor.username} - {self.period_start.date()} to {self.period_end.date()}"
