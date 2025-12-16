
# models.py
from django.db import models
from django.conf import settings
from django.utils import timezone
from users.models import CustomUser

class Statistics(models.Model):
    """Site-wide statistics"""
    active_students = models.IntegerField(default=0)
    courses = models.IntegerField(default=0)
    success_rate = models.IntegerField(default=0)
    tutors = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Statistics"
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"Statistics - Updated {self.updated_at.strftime('%Y-%m-%d')}"


class News(models.Model):
    """News articles"""
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='news/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True, help_text="Alternative to uploading image")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='news_articles')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "News"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    @property
    def get_image(self):
        """Return image URL or uploaded image"""
        if self.image:
            return self.image.url
        return self.image_url or '/api/placeholder/400/250'


class Event(models.Model):
    """Campus events"""
    title = models.CharField(max_length=255)
    content = models.TextField(help_text="Event details, date, time, location")
    video_id = models.CharField(max_length=100, blank=True, null=True, help_text="YouTube video ID")
    event_date = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-event_date', '-created_at']
    
    def __str__(self):
        return self.title


class Testimonial(models.Model):
    """Student/Alumni testimonials"""
    content = models.TextField(help_text="Testimonial quote")
    author = models.CharField(max_length=255)
    author_title = models.CharField(max_length=255, help_text="e.g., Computer Science Graduate, Class of 2023")
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True, help_text="Alternative to uploading image")
    email = models.EmailField(blank=True, null=True)
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='testimonials')
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.author} - {'Approved' if self.approved else 'Pending'}"
    
    @property
    def get_image(self):
        """Return image URL or uploaded image"""
        if self.image:
            return self.image.url
        return self.image_url or '/api/placeholder/100/100'


class CampusLife(models.Model):
    """Campus life gallery images"""
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='campus_life/')
    image_url = models.URLField(blank=True, null=True, help_text="Alternative to uploading image")
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='campus_images')
    created_at = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Campus Life"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title or f"Campus Image {self.id}"
    
    @property
    def get_image(self):
        """Return image URL or uploaded image"""
        if self.image:
            return self.image.url
        return self.image_url or '/api/placeholder/300/180'



class ContactMessage(models.Model):
    """Contact form submissions"""
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    replied = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.subject}"


# -------------------------------------
# Message System Models
# -------------------------------------
class Message(models.Model):
    """Tutor-Student-Admin communication system"""
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=255)
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    message_type = models.CharField(max_length=20, choices=[
        ('general', 'General'),
        ('assignment', 'Assignment'),
        ('grade', 'Grade'),
        ('announcement', 'Announcement'),
        ('support', 'Support')
    ], default='general')
    parent_message = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    course = models.ForeignKey('academics.Course', on_delete=models.CASCADE, null=True, blank=True, related_name='messages')
    assignment = models.ForeignKey('academics.Assignment', on_delete=models.CASCADE, null=True, blank=True, related_name='messages')
    
    class Meta:
        ordering = ['-sent_at']
    
    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}: {self.subject}"


class Notification(models.Model):
    """System-wide notification system"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_notifications', null=True, blank=True)
    type = models.CharField(max_length=20, choices=[
        ('announcement', 'Announcement'),
        ('assignment', 'Assignment'),
        ('grade', 'Grade'),
        ('class_update', 'Class Update'),
        ('deadline', 'Deadline'),
        ('system', 'System')
    ])
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ], default='medium')
    course = models.ForeignKey('academics.Course', on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    assignment = models.ForeignKey('academics.Assignment', on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username}: {self.title}"


class Announcement(models.Model):
    """Platform-wide announcements (Admin only)"""
    admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={"role": "admin"})
    title = models.CharField(max_length=255)
    content = models.TextField()
    target_audience = models.CharField(max_length=20, choices=[
        ('all', 'All Users'),
        ('students', 'Students Only'),
        ('tutors', 'Tutors Only'),
        ('admins', 'Admins Only')
    ], default='all')
    created_at = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent')
    ], default='medium')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.target_audience}"


# -------------------------------------
# Book Model for Digital Bookshelf
# -------------------------------------
class Book(models.Model):
    """Digital bookshelf books"""
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    cover_image = models.ImageField(upload_to='books/covers/', blank=True, null=True)
    pdf_file = models.FileField(upload_to='books/pdfs/', blank=True, null=True)
    isbn = models.CharField(max_length=20, blank=True, null=True)
    genre = models.CharField(max_length=100, blank=True, null=True)
    publication_year = models.IntegerField(blank=True, null=True)
    language = models.CharField(max_length=50, default='English')
    pages = models.IntegerField(blank=True, null=True)
    is_available = models.BooleanField(default=True)
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} by {self.author}"

    @property
    def get_cover_image(self):
        """Return cover image URL or placeholder"""
        if self.cover_image:
            return self.cover_image.url
        return '/api/placeholder/200/300'

    @property
    def get_pdf_file(self):
        """Return PDF file URL"""
        if self.pdf_file:
            return self.pdf_file.url
        return None
