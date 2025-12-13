# admin.py
from django.contrib import admin
from .models import Statistics, News, Event, Testimonial, CampusLife, ContactMessage


@admin.register(Statistics)
class StatisticsAdmin(admin.ModelAdmin):
    list_display = ['active_students', 'courses', 'success_rate', 'tutors', 'updated_at']
    fields = ['active_students', 'courses', 'success_rate', 'tutors']
    
    def has_add_permission(self, request):
        # Only allow one statistics record
        return not Statistics.objects.exists()


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'published', 'created_at']
    list_filter = ['published', 'created_at']
    search_fields = ['title', 'content']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'content', 'author')
        }),
        ('Media', {
            'fields': ('image', 'image_url')
        }),
        ('Publication', {
            'fields': ('published',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_date', 'location', 'published', 'created_at']
    list_filter = ['published', 'event_date', 'created_at']
    search_fields = ['title', 'content', 'location']
    date_hierarchy = 'event_date'
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Event Details', {
            'fields': ('title', 'content', 'event_date', 'location')
        }),
        ('Media', {
            'fields': ('video_id',)
        }),
        ('Publication', {
            'fields': ('published',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['author', 'author_title', 'approved', 'email', 'created_at']
    list_filter = ['approved', 'created_at']
    search_fields = ['author', 'author_title', 'content', 'email']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at', 'submitted_by']
    actions = ['approve_testimonials', 'unapprove_testimonials']
    
    fieldsets = (
        ('Testimonial Content', {
            'fields': ('content', 'author', 'author_title')
        }),
        ('Contact', {
            'fields': ('email',)
        }),
        ('Media', {
            'fields': ('image', 'image_url')
        }),
        ('Approval', {
            'fields': ('approved',)
        }),
        ('Metadata', {
            'fields': ('submitted_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def approve_testimonials(self, request, queryset):
        updated = queryset.update(approved=True)
        self.message_user(request, f'{updated} testimonial(s) approved.')
    approve_testimonials.short_description = 'Approve selected testimonials'
    
    def unapprove_testimonials(self, request, queryset):
        updated = queryset.update(approved=False)
        self.message_user(request, f'{updated} testimonial(s) unapproved.')
    unapprove_testimonials.short_description = 'Unapprove selected testimonials'


@admin.register(CampusLife)
class CampusLifeAdmin(admin.ModelAdmin):
    list_display = ['title', 'uploaded_by', 'published', 'created_at']
    list_filter = ['published', 'created_at']
    search_fields = ['title', 'description']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'uploaded_by']
    
    fieldsets = (
        ('Image Details', {
            'fields': ('title', 'description')
        }),
        ('Media', {
            'fields': ('image', 'image_url')
        }),
        ('Publication', {
            'fields': ('published',)
        }),
        ('Metadata', {
            'fields': ('uploaded_by', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'read', 'replied', 'created_at']
    list_filter = ['read', 'replied', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    date_hierarchy = 'created_at'
    readonly_fields = ['name', 'email', 'subject', 'message', 'created_at']
    actions = ['mark_as_read', 'mark_as_replied']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'subject')
        }),
        ('Message', {
            'fields': ('message',)
        }),
        ('Status', {
            'fields': ('read', 'replied')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def mark_as_read(self, request, queryset):
        updated = queryset.update(read=True)
        self.message_user(request, f'{updated} message(s) marked as read.')
    mark_as_read.short_description = 'Mark as read'
    
    def mark_as_replied(self, request, queryset):
        updated = queryset.update(replied=True)
        self.message_user(request, f'{updated} message(s) marked as replied.')
    mark_as_replied.short_description = 'Mark as replied'