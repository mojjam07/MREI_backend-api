from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

# -------------------------------------
# Main User Model
# -------------------------------------
class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='customuser_set',
        related_query_name='customuser',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='customuser_set',
        related_query_name='customuser',
    )

    ROLE_CHOICES = [
        ("student", "Student"),
        ("tutor", "Tutor"),
        ("alumni", "Alumni"),
        ("admin", "Admin"),
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="student")
    preferred_language = models.CharField(max_length=10, default="en")  # en | ar
    profile_image = models.URLField(blank=True, null=True)

    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return f"{self.username} - {self.role}"


# -------------------------------------
# Student Profile
# -------------------------------------
class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="student_profile")
    student_number = models.CharField(max_length=20, unique=True)
    course_of_study = models.CharField(max_length=255)
    admission_year = models.IntegerField()
    status = models.CharField(max_length=20, default="active")

    def __str__(self):
        return self.student_number


# -------------------------------------
# Tutor Profile
# -------------------------------------
class TutorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="tutor_profile")
    staff_number = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=255)
    bio = models.TextField(blank=True, null=True)
    subjects = models.TextField(help_text="Comma-separated list of courses/subjects")

    def __str__(self):
        return self.staff_number


# -------------------------------------
# Admin Profile
# -------------------------------------
class AdminProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="admin_profile")
    role_title = models.CharField(max_length=255)
    department = models.CharField(max_length=255)

    def __str__(self):
        return self.role_title


# -------------------------------------
# Alumni Profile
# -------------------------------------
class AlumniProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="alumni_profile")
    graduation_year = models.IntegerField()
    current_employer = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} Alumni"
