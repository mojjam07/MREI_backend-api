from django.contrib import admin
from .models import CustomUser, StudentProfile, TutorProfile, AdminProfile, AlumniProfile

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(StudentProfile)
admin.site.register(TutorProfile)
admin.site.register(AdminProfile)
admin.site.register(AlumniProfile)
