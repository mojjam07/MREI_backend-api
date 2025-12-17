from django.contrib import admin
from django.utils.html import format_html
from .models import Course, Enrollment, Assignment, AssignmentSubmission, Attendance, ClassSchedule, TutorPerformance

# -------------------------------------
# Course Admin
# -------------------------------------
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'title', 'tutor', 'credit_hours', 'is_active', 'created_at']
    list_filter = ['is_active', 'credit_hours', 'created_at']
    search_fields = ['code', 'title', 'description', 'tutor']
    readonly_fields = ['created_at', 'updated_at']
    

    fieldsets = (
        ('Course Information', {
            'fields': ('code', 'title', 'description')
        }),
        ('Instructor & Credits', {
            'fields': ('tutor', 'credit_hours')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

# -------------------------------------
# Enrollment Admin
# -------------------------------------
@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'enrolled_at', 'status', 'grade']
    list_filter = ['status', 'enrolled_at', 'course']
    search_fields = ['student__username', 'student__email', 'course__title', 'course__code']
    readonly_fields = ['enrolled_at']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('student', 'course')

# -------------------------------------
# Assignment Admin
# -------------------------------------
@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'assignment_type', 'due_date', 'max_points', 'created_at']
    list_filter = ['assignment_type', 'due_date', 'course', 'created_at']
    search_fields = ['title', 'description', 'course__title']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'due_date'
    
    fieldsets = (
        ('Assignment Details', {
            'fields': ('title', 'description', 'course')
        }),
        ('Assignment Info', {
            'fields': ('assignment_type', 'due_date', 'max_points')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

# -------------------------------------
# Assignment Submission Admin
# -------------------------------------
@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ['assignment', 'student', 'submitted_at', 'grade', 'is_graded_display', 'is_late_display']
    list_filter = ['assignment__course', 'submitted_at', 'status']
    search_fields = ['student__username', 'assignment__title']
    readonly_fields = ['submitted_at']
    date_hierarchy = 'submitted_at'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('student', 'assignment', 'assignment__course')

    def is_graded_display(self, obj):
        return obj.is_graded
    is_graded_display.boolean = True
    is_graded_display.short_description = 'Graded'

    def is_late_display(self, obj):
        return obj.is_late
    is_late_display.boolean = True
    is_late_display.short_description = 'Late'

# -------------------------------------
# Attendance Admin
# -------------------------------------
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'class_schedule__course', 'attended_at', 'status']
    list_filter = ['status', 'attended_at', 'class_schedule__course']
    search_fields = ['student__username', 'student__email', 'class_schedule__course__title']
    readonly_fields = ['attended_at']
    date_hierarchy = 'attended_at'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('student', 'class_schedule__course')


# -------------------------------------
# Class Schedule Admin
# -------------------------------------
@admin.register(ClassSchedule)
class ClassScheduleAdmin(admin.ModelAdmin):
    list_display = ['course', 'tutor', 'title', 'scheduled_date', 'class_type']
    list_filter = ['course', 'tutor', 'class_type', 'scheduled_date']
    search_fields = ['title', 'description', 'course__title']
    readonly_fields = ['created_at']

    fieldsets = (
        ('Schedule Details', {
            'fields': ('course', 'tutor', 'title', 'description')
        }),
        ('Schedule Info', {
            'fields': ('scheduled_date', 'duration_minutes', 'class_type')
        }),
        ('Meeting Details', {
            'fields': ('meeting_link', 'attendance_tracking')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


# -------------------------------------
# Tutor Performance Admin
# -------------------------------------
@admin.register(TutorPerformance)
class TutorPerformanceAdmin(admin.ModelAdmin):
    list_display = ['tutor', 'period_start', 'period_end', 'students_managed', 'avg_rating', 'attendance_rate']
    list_filter = ['tutor', 'period_start', 'period_end', 'avg_rating']
    search_fields = ['tutor__username', 'tutor__email']
    readonly_fields = ['created_at']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('tutor')
