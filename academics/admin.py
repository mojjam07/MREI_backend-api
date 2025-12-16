from django.contrib import admin

from .models import Course, Enrollment, Assignment, AssignmentSubmission, Attendance, ClassSchedule, TutorPerformance



# Register your models here.
admin.site.register(Course)
admin.site.register(Enrollment)
admin.site.register(Assignment)
admin.site.register(AssignmentSubmission)
admin.site.register(Attendance)
admin.site.register(ClassSchedule)
admin.site.register(TutorPerformance)
