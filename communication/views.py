# views.py

from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Statistics, News, Event, Testimonial, CampusLife, ContactMessage, Message, Notification, Announcement, Book
from academics.models import Course, Assignment, ClassSchedule, Enrollment
from .serializers import (
    StatisticsSerializer, NewsSerializer, EventSerializer, TestimonialSerializer,
    CampusLifeSerializer, ContactMessageSerializer, MessageSerializer,
    NotificationSerializer, AnnouncementSerializer, BookSerializer
)

User = get_user_model()

# -------------------------------------
# ViewSets
# -------------------------------------

class StatisticsViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing statistics
    """
    queryset = Statistics.objects.all()
    serializer_class = StatisticsSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        """
        Set permissions based on action
        """
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class NewsViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing news articles
    """
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Return only published news for non-admin users
        """
        if self.request.user.is_staff or self.request.user.is_superuser:
            return News.objects.all()
        return News.objects.filter(published=True)
    
    def get_permissions(self):
        """
        Set permissions based on action
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class EventViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing events
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Return only published events for non-admin users
        """
        if self.request.user.is_staff or self.request.user.is_superuser:
            return Event.objects.all()
        return Event.objects.filter(published=True)
    
    def get_permissions(self):
        """
        Set permissions based on action
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class TestimonialViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing testimonials
    """
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Return only approved testimonials for non-admin users
        """
        if self.request.user.is_staff or self.request.user.is_superuser:
            return Testimonial.objects.all()
        return Testimonial.objects.filter(approved=True)
    
    def get_permissions(self):
        """
        Set permissions based on action
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class CampusLifeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing campus life images
    """
    queryset = CampusLife.objects.all()
    serializer_class = CampusLifeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Return only published images for non-admin users
        """
        if self.request.user.is_staff or self.request.user.is_superuser:
            return CampusLife.objects.all()
        return CampusLife.objects.filter(published=True)
    
    def get_permissions(self):
        """
        Set permissions based on action
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class ContactMessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing contact messages (admin only)
    """
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [IsAdminUser]
    

    def get_permissions(self):
        """
        Only admin users can access contact messages
        """
        permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


# -------------------------------------
# Function Views
# -------------------------------------

@api_view(['GET'])
@permission_classes([AllowAny])
def get_home_content(request):
    """
    Get content for the homepage (news, events, statistics, testimonials)
    """
    try:
        # Get latest statistics
        latest_stats = Statistics.objects.first()
        
        # Get latest published news (limit to 3)
        latest_news = News.objects.filter(published=True).order_by('-created_at')[:3]
        
        # Get upcoming events (limit to 3)
        upcoming_events = Event.objects.filter(
            published=True,
            event_date__gte=timezone.now()
        ).order_by('event_date')[:3]
        
        # Get approved testimonials (limit to 3)
        testimonials = Testimonial.objects.filter(approved=True).order_by('-created_at')[:3]
        
        # Get campus life images (limit to 6)
        campus_images = CampusLife.objects.filter(published=True).order_by('-created_at')[:6]
        
        # Serialize the data
        stats_data = StatisticsSerializer(latest_stats).data if latest_stats else None
        news_data = NewsSerializer(latest_news, many=True).data
        events_data = EventSerializer(upcoming_events, many=True).data
        testimonials_data = TestimonialSerializer(testimonials, many=True).data
        campus_data = CampusLifeSerializer(campus_images, many=True).data
        
        return Response({
            'statistics': stats_data,
            'news': news_data,
            'events': events_data,
            'testimonials': testimonials_data,
            'campus_life': campus_data
        })
        
    except Exception as e:
        return Response({
            'error': 'Failed to fetch home content',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """
    Get dashboard statistics for the current user
    """
    try:
        user = request.user
        stats = {}
        
        if user.role == 'student':
            # Student stats
            enrollments = Enrollment.objects.filter(student=user)
            stats['total_courses'] = enrollments.count()
            stats['active_courses'] = enrollments.filter(is_active=True).count()
            stats['completed_courses'] = enrollments.filter(is_active=False).count()
            
            # Recent assignments
            recent_assignments = Assignment.objects.filter(
                course__enrollments__student=user
            ).order_by('-due_date')[:5]
            stats['recent_assignments'] = [
                {
                    'id': assignment.id,
                    'title': assignment.title,
                    'course': assignment.course.title,
                    'due_date': assignment.due_date
                }
                for assignment in recent_assignments
            ]
            
        elif user.role == 'tutor':
            # Tutor stats
            courses = Course.objects.filter(tutor=user)
            stats['total_courses'] = courses.count()
            stats['active_courses'] = courses.filter(is_active=True).count()
            stats['total_students'] = Enrollment.objects.filter(course__in=courses).count()
            
            # Recent submissions
            recent_submissions = AssignmentSubmission.objects.filter(
                assignment__course__tutor=user
            ).order_by('-submitted_at')[:5]
            stats['recent_submissions'] = [
                {
                    'id': submission.id,
                    'assignment': submission.assignment.title,
                    'student': submission.student.username,
                    'submitted_at': submission.submitted_at
                }
                for submission in recent_submissions
            ]
            
        elif user.role == 'admin':
            # Admin stats
            from users.models import CustomUser
            stats['total_users'] = CustomUser.objects.count()
            stats['total_students'] = CustomUser.objects.filter(role='student').count()
            stats['total_tutors'] = CustomUser.objects.filter(role='tutor').count()
            stats['total_courses'] = Course.objects.count()
            stats['total_assignments'] = Assignment.objects.count()
            
            # Recent messages
            recent_messages = ContactMessage.objects.order_by('-created_at')[:5]
            stats['recent_messages'] = [
                {
                    'id': message.id,
                    'name': message.name,
                    'subject': message.subject,
                    'created_at': message.created_at,
                    'read': message.read
                }
                for message in recent_messages
            ]
        
        return Response(stats)
        
    except Exception as e:
        return Response({
            'error': 'Failed to fetch dashboard stats',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['GET'])
@permission_classes([AllowAny])
def global_search(request):
    """
    Global search endpoint that searches across multiple models
    """
    query = request.GET.get('q', '').strip()
    
    if not query:
        return Response({
            'results': {
                'courses': [],
                'assignments': [],
                'news': [],
                'events': [],
                'users': [],
                'announcements': []
            },
            'total_results': 0
        })
    
    # Search courses
    courses = Course.objects.filter(
        Q(title__icontains=query) |
        Q(code__icontains=query) |
        Q(description__icontains=query) |
        Q(subject__icontains=query),
        is_active=True
    ).select_related('tutor')[:10]
    
    course_results = []
    for course in courses:
        course_results.append({
            'id': course.id,
            'title': course.title,
            'type': 'course',
            'subtitle': f"{course.code} - {course.subject or 'General'}",
            'description': course.description[:100] + '...' if course.description else '',
            'tutor': course.tutor.username if course.tutor else 'Unassigned',
            'url': f'/courses/{course.id}',
            'match_highlights': {
                'title': query if query.lower() in course.title.lower() else None,
                'code': query if query.lower() in course.code.lower() else None
            }
        })
    
    # Search assignments
    assignments = Assignment.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(instructions__icontains=query)
    ).select_related('course', 'tutor')[:10]
    
    assignment_results = []
    for assignment in assignments:
        assignment_results.append({
            'id': assignment.id,
            'title': assignment.title,
            'type': 'assignment',
            'subtitle': f"{assignment.course.code} - {assignment.course.title}",
            'description': assignment.description[:100] + '...' if assignment.description else '',
            'tutor': assignment.tutor.username,
            'due_date': assignment.due_date,
            'url': f'/assignments/{assignment.id}',
            'match_highlights': {
                'title': query if query.lower() in assignment.title.lower() else None,
                'description': query if query.lower() in (assignment.description or '').lower() else None
            }
        })
    
    # Search news
    news = News.objects.filter(
        Q(title__icontains=query) |
        Q(content__icontains=query),
        published=True
    ).select_related('author')[:10]
    
    news_results = []
    for article in news:
        news_results.append({
            'id': article.id,
            'title': article.title,
            'type': 'news',
            'subtitle': f"Published {article.created_at.strftime('%B %d, %Y')}",
            'description': article.content[:150] + '...' if article.content else '',
            'author': article.author.username if article.author else 'Staff',
            'image_url': article.get_image,
            'url': f'/news/{article.id}',
            'match_highlights': {
                'title': query if query.lower() in article.title.lower() else None,
                'content': query if query.lower() in article.content[:200].lower() else None
            }
        })
    
    # Search events
    events = Event.objects.filter(
        Q(title__icontains=query) |
        Q(content__icontains=query) |
        Q(location__icontains=query),
        published=True
    )[:10]
    
    event_results = []
    for event in events:
        event_results.append({
            'id': event.id,
            'title': event.title,
            'type': 'event',
            'subtitle': f"{event.location or 'TBD'} - {event.event_date.strftime('%B %d, %Y') if event.event_date else 'Date TBD'}",
            'description': event.content[:150] + '...' if event.content else '',
            'event_date': event.event_date,
            'location': event.location,
            'url': f'/events/{event.id}',
            'match_highlights': {
                'title': query if query.lower() in event.title.lower() else None,
                'location': query if query.lower() in (event.location or '').lower() else None
            }
        })
    
    # Search users (for admin/staff)
    users = User.objects.filter(
        Q(username__icontains=query) |
        Q(first_name__icontains=query) |
        Q(last_name__icontains=query) |
        Q(email__icontains=query)
    )[:10]
    
    user_results = []
    for user in users:
        user_results.append({
            'id': user.id,
            'title': f"{user.first_name} {user.last_name}".strip() or user.username,
            'type': 'user',
            'subtitle': f"{user.role.title()} - {user.email}",
            'description': f"Username: {user.username}",
            'role': user.role,
            'email': user.email,
            'url': f'/users/{user.id}',
            'match_highlights': {
                'name': query if query.lower() in user.username.lower() or query.lower() in f"{user.first_name} {user.last_name}".lower() else None,
                'email': query if query.lower() in user.email.lower() else None
            }
        })
    
    # Search announcements
    announcements = Announcement.objects.filter(
        Q(title__icontains=query) |
        Q(content__icontains=query),
        published=True
    ).select_related('admin')[:10]
    
    announcement_results = []
    for announcement in announcements:
        announcement_results.append({
            'id': announcement.id,
            'title': announcement.title,
            'type': 'announcement',
            'subtitle': f"{announcement.target_audience.title()} - {announcement.created_at.strftime('%B %d, %Y')}",
            'description': announcement.content[:150] + '...' if announcement.content else '',
            'admin': announcement.admin.username,
            'priority': announcement.priority,
            'url': f'/announcements/{announcement.id}',
            'match_highlights': {
                'title': query if query.lower() in announcement.title.lower() else None,
                'content': query if query.lower() in announcement.content[:200].lower() else None
            }
        })
    
    # Compile results
    results = {
        'courses': course_results,
        'assignments': assignment_results,
        'news': news_results,
        'events': event_results,
        'users': user_results,
        'announcements': announcement_results
    }
    
    # Calculate total results
    total_results = (
        len(course_results) + 
        len(assignment_results) + 
        len(news_results) + 
        len(event_results) + 
        len(user_results) + 
        len(announcement_results)
    )
    
    return Response({
        'query': query,
        'results': results,
        'total_results': total_results,
        'search_time': timezone.now().isoformat()
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def quick_search(request):
    """
    Quick search for suggestions/autocomplete
    """
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return Response({'suggestions': []})
    
    suggestions = []
    
    # Course suggestions
    course_suggestions = Course.objects.filter(
        Q(title__icontains=query) |
        Q(code__icontains=query),
        is_active=True
    )[:5]
    
    for course in course_suggestions:
        suggestions.append({
            'text': f"{course.code} - {course.title}",
            'type': 'course',
            'id': course.id
        })
    
    # Assignment suggestions
    assignment_suggestions = Assignment.objects.filter(
        title__icontains=query
    )[:3]
    
    for assignment in assignment_suggestions:
        suggestions.append({
            'text': f"Assignment: {assignment.title}",
            'type': 'assignment',
            'id': assignment.id
        })
    
    # News suggestions
    news_suggestions = News.objects.filter(
        title__icontains=query,
        published=True
    )[:3]
    
    for article in news_suggestions:
        suggestions.append({
            'text': f"News: {article.title}",
            'type': 'news',
            'id': article.id
        })
    
    return Response({
        'query': query,
        'suggestions': suggestions[:10]
    })


class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing digital bookshelf books
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return only available books for non-admin users
        """
        if self.request.user.is_staff or self.request.user.is_superuser:
            return Book.objects.all()
        return Book.objects.filter(is_available=True)

    def get_permissions(self):
        """
        Set permissions based on action
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """
        Set the uploaded_by field when creating a book
        """
        serializer.save(uploaded_by=self.request.user)


# ... existing views remain the same ...
