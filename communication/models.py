from django.db import models
from users.models import CustomUser


# -------------------------------------
# Announcements
# -------------------------------------
class Announcement(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    visible_to = models.CharField(
        max_length=20,
        choices=[
            ("everyone", "Everyone"),
            ("students", "Students"),
            ("tutors", "Tutors"),
            ("staff", "Staff"),
        ],
        default="everyone"
    )
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.title

# -------------------------------------
# Messages
# -------------------------------------

class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"


# -------------------------------------
# Notifications
# -------------------------------------
class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    message = models.TextField()
    type = models.CharField(max_length=50, default="general")
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
