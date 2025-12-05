from django.db import models
from users.models import CustomUser, StudentProfile, TutorProfile


# -------------------------------------
# Course Model
# -------------------------------------
class Course(models.Model):
    code = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    tutor = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, limit_choices_to={"role": "tutor"})
    credit_hours = models.IntegerField(default=3)

    def __str__(self):
        return f"{self.code} - {self.title}"


# -------------------------------------
# Enrollment
# -------------------------------------
class Enrollment(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={"role": "student"})
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default="enrolled")
    grade = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        unique_together = ("student", "course")

    def __str__(self):
        return f"{self.student.username} -> {self.course.code}"


# -------------------------------------
# Assignment
# -------------------------------------
class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField()
    attachment_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title


# -------------------------------------
# Submission
# -------------------------------------
class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={"role": "student"})
    file_url = models.URLField()
    grade = models.CharField(max_length=5, blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.assignment.title} -> {self.student.username}"


# -------------------------------------
# Attendance
# -------------------------------------
class Attendance(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name="attendance_records")
    date = models.DateField()
    present = models.BooleanField(default=False)

    class Meta:
        unique_together = ("enrollment", "date")

    def __str__(self):
        return f"{self.enrollment.student.username} - {self.date}"
