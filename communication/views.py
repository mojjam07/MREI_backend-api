# views.py
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from .models import Statistics, News, Event, Testimonial, CampusLife, ContactMessage
from .serializers import StatisticSerializer, NewsSerializer, EventSerializer, TestimonialSerializer, TestimonialSerializer, CampusLifeSerializer, ContactMessageSerializer


# ============================================================================
# STATISTICS VIEWSET
# ============================================================================
class StatisticsViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing site statistics.
    
    Permissions:
    - GET (list, retrieve): Public access
    - POST, PUT, PATCH, DELETE: Admin only
    
    Endpoints:
    - GET /api/statistics/ - List all statistics
    - GET /api/statistics/{id}/ - Get specific statistics
    - GET /api/statistics/latest/ - Get latest statistics (custom action)
    - POST /api/statistics/ - Create statistics (admin)
    - PUT/PATCH /api/statistics/{id}/ - Update statistics (admin)
    - DELETE /api/statistics/{id}/ - Delete statistics (admin)
    """
    queryset = Statistics.objects.all()
    serializer_class = StatisticSerializer
    
    def get_permissions(self):
        """
        Public can view, only admins can modify
        """
        if self.action in ['list', 'retrieve', 'latest']:
            return [AllowAny()]
        return [IsAdminUser()]
    
    def list(self, request, *args, **kwargs):
        """
        List all statistics records
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        """
        Get a specific statistics record
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """
        Create new statistics record (admin only)
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        """
        Update statistics record (admin only)
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, *args, **kwargs):
        """
        Partially update statistics record (admin only)
        """
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """
        Delete statistics record (admin only)
        """
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def latest(self, request):
        """
        Get the latest/most recent statistics record
        
        GET /api/statistics/latest/
        """
        stats = self.queryset.first()
        if stats:
            serializer = self.get_serializer(stats)
            return Response(serializer.data)
        return Response({
            'active_students': 0,
            'courses': 0,
            'success_rate': 0,
            'tutors': 0
        })


# ============================================================================
# NEWS VIEWSET
# ============================================================================
class NewsViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing news articles.
    
    Permissions:
    - GET (list, retrieve): Public access (published only)
    - POST, PUT, PATCH, DELETE: Admin only
    
    Endpoints:
    - GET /api/news/ - List published news
    - GET /api/news/?published=true/false - Filter by published status
    - GET /api/news/{id}/ - Get specific news article
    - POST /api/news/ - Create news article (admin)
    - PUT/PATCH /api/news/{id}/ - Update news article (admin)
    - DELETE /api/news/{id}/ - Delete news article (admin)
    """
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['published']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_permissions(self):
        """
        Public can view published news, only admins can modify
        """
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]
    
    def get_queryset(self):
        """
        Filter queryset based on user permissions
        - Admin: sees all news
        - Public: sees only published news
        """
        queryset = self.queryset
        if not self.request.user.is_staff:
            queryset = queryset.filter(published=True)
        return queryset
    
    def list(self, request, *args, **kwargs):
        """
        List news articles
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        """
        Get a specific news article
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """
        Create a new news article (admin only)
        Automatically sets the author to the current user
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        """
        Update a news article (admin only)
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, *args, **kwargs):
        """
        Partially update a news article (admin only)
        """
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """
        Delete a news article (admin only)
        """
        instance = self.get_object()
        instance.delete()
        return Response({
            'success': True,
            'message': 'News article deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)


# ============================================================================
# EVENT VIEWSET
# ============================================================================
class EventViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing campus events.
    
    Permissions:
    - GET (list, retrieve): Public access (published only)
    - POST, PUT, PATCH, DELETE: Admin only
    
    Endpoints:
    - GET /api/events/ - List published events
    - GET /api/events/?published=true/false - Filter by published status
    - GET /api/events/{id}/ - Get specific event
    - POST /api/events/ - Create event (admin)
    - PUT/PATCH /api/events/{id}/ - Update event (admin)
    - DELETE /api/events/{id}/ - Delete event (admin)
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['published']
    search_fields = ['title', 'content', 'location']
    ordering_fields = ['event_date', 'created_at']
    ordering = ['-event_date', '-created_at']
    
    def get_permissions(self):
        """
        Public can view published events, only admins can modify
        """
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]
    
    def get_queryset(self):
        """
        Filter queryset based on user permissions
        - Admin: sees all events
        - Public: sees only published events
        """
        queryset = self.queryset
        if self.request.user.role != 'admin':
            queryset = queryset.filter(published=True)
        return queryset
    
    def list(self, request, *args, **kwargs):
        """
        List events
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        """
        Get a specific event
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """
        Create a new event (admin only)
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        """
        Update an event (admin only)
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, *args, **kwargs):
        """
        Partially update an event (admin only)
        """
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """
        Delete an event (admin only)
        """
        instance = self.get_object()
        instance.delete()
        return Response({
            'success': True,
            'message': 'Event deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)


# ============================================================================
# TESTIMONIAL VIEWSET
# ============================================================================
class TestimonialViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing testimonials.
    
    Permissions:
    - GET (list, retrieve): Public access (approved only)
    - POST: Admin only (for admin-created testimonials)
    - POST /submit/: Public access (for user submissions)
    - PUT, PATCH, DELETE: Admin only
    
    Endpoints:
    - GET /api/testimonials/ - List approved testimonials
    - GET /api/testimonials/?approved=true/false - Filter by approval
    - GET /api/testimonials/{id}/ - Get specific testimonial
    - POST /api/testimonials/ - Create testimonial (admin)
    - POST /api/testimonials/submit/ - Submit testimonial (public)
    - PUT/PATCH /api/testimonials/{id}/ - Update testimonial (admin)
    - DELETE /api/testimonials/{id}/ - Delete testimonial (admin)
    - POST /api/testimonials/{id}/approve/ - Approve testimonial (admin)
    - POST /api/testimonials/{id}/unapprove/ - Unapprove testimonial (admin)
    - PATCH /api/testimonials/{id}/toggle_approval/ - Toggle approval (admin)
    """
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['approved']
    search_fields = ['author', 'author_title', 'content']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_permissions(self):
        """
        Set permissions based on action
        """
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        elif self.action == 'submit':
            return [AllowAny()]
        return [IsAdminUser()]
    
    def get_queryset(self):
        """
        Filter queryset based on user permissions
        - Admin: sees all testimonials
        - Public: sees only approved testimonials
        """
        queryset = self.queryset
        
        # Non-admin users only see approved testimonials
        if not self.request.user.is_staff:
            queryset = queryset.filter(approved=True)
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        """
        List testimonials
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        """
        Get a specific testimonial
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """
        Create a new testimonial (admin only)
        Admin-created testimonials are automatically approved
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Admin-created testimonials default to approved
            serializer.save(
                submitted_by=request.user,
                approved=request.data.get('approved', True)
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        """
        Update a testimonial (admin only)
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, *args, **kwargs):
        """
        Partially update a testimonial (admin only)
        """
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """
        Delete a testimonial (admin only)
        """
        instance = self.get_object()
        instance.delete()
        return Response({
            'success': True,
            'message': 'Testimonial deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def submit(self, request):
        """
        Public endpoint for submitting testimonials
        Testimonials submitted through this endpoint start as unapproved
        
        POST /api/testimonials/submit/
        
        Request body:
        {
            "content": "Testimonial text",
            "author": "John Doe",
            "author_title": "Computer Science Graduate",
            "email": "john@example.com",
            "image_url": "https://example.com/image.jpg"
        }
        """
        serializer = TestimonialSubmitSerializer(data=request.data)
        if serializer.is_valid():
            testimonial = serializer.save()
            return Response({
                'success': True,
                'message': 'Thank you! Your testimonial has been submitted and is pending approval.',
                'id': testimonial.id
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def approve(self, request, pk=None):
        """
        Approve a testimonial
        
        POST /api/testimonials/{id}/approve/
        """
        testimonial = self.get_object()
        testimonial.approved = True
        testimonial.save()
        serializer = self.get_serializer(testimonial)
        return Response({
            'success': True,
            'message': 'Testimonial approved successfully',
            'data': serializer.data
        })
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def unapprove(self, request, pk=None):
        """
        Unapprove a testimonial
        
        POST /api/testimonials/{id}/unapprove/
        """
        testimonial = self.get_object()
        testimonial.approved = False
        testimonial.save()
        serializer = self.get_serializer(testimonial)
        return Response({
            'success': True,
            'message': 'Testimonial unapproved successfully',
            'data': serializer.data
        })
    
    @action(detail=True, methods=['patch'], permission_classes=[IsAdminUser])
    def toggle_approval(self, request, pk=None):
        """
        Toggle testimonial approval status
        
        PATCH /api/testimonials/{id}/toggle_approval/
        """
        testimonial = self.get_object()
        testimonial.approved = not testimonial.approved
        testimonial.save()
        serializer = self.get_serializer(testimonial)
        return Response({
            'success': True,
            'message': f'Testimonial {"approved" if testimonial.approved else "unapproved"} successfully',
            'data': serializer.data
        })


# ============================================================================
# CAMPUS LIFE VIEWSET
# ============================================================================
class CampusLifeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing campus life gallery images.
    
    Permissions:
    - GET (list, retrieve): Public access (published only)
    - POST, PUT, PATCH, DELETE: Admin only
    
    Endpoints:
    - GET /api/campus-life/ - List published images
    - GET /api/campus-life/?published=true/false - Filter by published status
    - GET /api/campus-life/{id}/ - Get specific image
    - POST /api/campus-life/ - Upload image (admin)
    - PUT/PATCH /api/campus-life/{id}/ - Update image (admin)
    - DELETE /api/campus-life/{id}/ - Delete image (admin)
    """
    queryset = CampusLife.objects.all()
    serializer_class = CampusLifeSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['published']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_permissions(self):
        """
        Public can view published images, only admins can modify
        """
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]
    
    def get_queryset(self):
        """
        Filter queryset based on user permissions
        - Admin: sees all images
        - Public: sees only published images
        """
        queryset = self.queryset
        if self.request.user.role != 'admin':
            queryset = queryset.filter(published=True)
        return queryset
    
    def list(self, request, *args, **kwargs):
        """
        List campus life images
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        """
        Get a specific campus life image
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """
        Upload a new campus life image (admin only)
        Automatically sets uploaded_by to current user
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(uploaded_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        """
        Update a campus life image (admin only)
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, *args, **kwargs):
        """
        Partially update a campus life image (admin only)
        """
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """
        Delete a campus life image (admin only)
        """
        instance = self.get_object()
        instance.delete()
        return Response({
            'success': True,
            'message': 'Campus life image deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)


# ============================================================================
# CONTACT MESSAGE VIEWSET
# ============================================================================
class ContactMessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing contact form submissions.
    
    Permissions:
    - POST: Public access (anyone can submit)
    - GET, PUT, PATCH, DELETE: Admin only
    
    Endpoints:
    - GET /api/contact/ - List all messages (admin)
    - GET /api/contact/?read=true/false - Filter by read status
    - GET /api/contact/{id}/ - Get specific message (admin)
    - POST /api/contact/ - Submit contact form (public)
    - PUT/PATCH /api/contact/{id}/ - Update message (admin)
    - DELETE /api/contact/{id}/ - Delete message (admin)
    - POST /api/contact/{id}/mark_read/ - Mark as read (admin)
    - POST /api/contact/{id}/mark_replied/ - Mark as replied (admin)
    """
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['read', 'replied']
    search_fields = ['name', 'email', 'subject', 'message']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_permissions(self):
        """
        Public can create, only admins can view and manage
        """
        if self.action == 'create':
            return [AllowAny()]
        return [IsAdminUser()]
    
    def get_serializer_class(self):
        """
        Use different serializer for creation
        """
        if self.action == 'create':
            return ContactMessageCreateSerializer
        return ContactMessageSerializer
    
    def list(self, request, *args, **kwargs):
        """
        List all contact messages (admin only)
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        """
        Get a specific contact message (admin only)
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """
        Submit a contact form message (public)
        
        POST /api/contact/
        
        Request body:
        {
            "name": "John Doe",
            "email": "john@example.com",
            "subject": "Inquiry",
            "message": "Message content"
        }
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'Your message has been sent successfully. We will get back to you soon!'
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        """
        Update a contact message (admin only)
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, *args, **kwargs):
        """
        Partially update a contact message (admin only)
        """
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """
        Delete a contact message (admin only)
        """
        instance = self.get_object()
        instance.delete()
        return Response({
            'success': True,
            'message': 'Contact message deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def mark_read(self, request, pk=None):
        """
        Mark a contact message as read
        
        POST /api/contact/{id}/mark_read/
        """
        message = self.get_object()
        message.read = True
        message.save()
        serializer = self.get_serializer(message)
        return Response({
            'success': True,
            'message': 'Message marked as read',
            'data': serializer.data
        })
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def mark_replied(self, request, pk=None):
        """
        Mark a contact message as replied
        
        POST /api/contact/{id}/mark_replied/
        """
        message = self.get_object()
        message.replied = True
        message.save()
        serializer = self.get_serializer(message)
        return Response({
            'success': True,
            'message': 'Message marked as replied',
            'data': serializer.data
        })
    
    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def unread(self, request):
        """
        Get all unread messages
        
        GET /api/contact/unread/
        """
        unread_messages = self.queryset.filter(read=False)
        serializer = self.get_serializer(unread_messages, many=True)
        return Response({
            'count': unread_messages.count(),
            'results': serializer.data
        })


# ============================================================================
# COMBINED HOME CONTENT VIEW
# ============================================================================

@api_view(['GET'])
@permission_classes([AllowAny])
def get_home_content(request):
    """
    Get all content for home page in a single request.
    This endpoint combines data from multiple models to reduce API calls.
    
    GET /api/home-content/
    
    Returns:
    {
        "stats": {...},
        "news": [...],
        "events": [...],
        "testimonials": [...],
        "campus_life": [...]
    }
    """
    # Get latest statistics
    stats = Statistics.objects.first()
    
    # Get published content
    news = News.objects.filter(published=True).order_by('-created_at')[:3]
    events = Event.objects.filter(published=True).order_by('-event_date', '-created_at')[:3]
    testimonials = Testimonial.objects.filter(approved=True).order_by('-created_at')[:3]
    campus_life = CampusLife.objects.filter(published=True).order_by('-created_at')[:8]
    
    return Response({
        'stats': StatisticSerializer(stats).data if stats else {
            'active_students': 0,
            'courses': 0,
            'success_rate': 0,
            'tutors': 0
        },
        'news': NewsSerializer(news, many=True).data,
        'events': EventSerializer(events, many=True).data,
        'testimonials': TestimonialSerializer(testimonials, many=True).data,
        'campus_life': CampusLifeSerializer(campus_life, many=True).data,
    })


# ============================================================================
# UTILITY VIEWS
# ============================================================================
@api_view(['GET'])
@permission_classes([IsAdminUser])
def dashboard_stats(request):
    """
    Get dashboard statistics for admin
    
    GET /api/dashboard-stats/
    
    Returns counts of various content types
    """
    return Response({
        'total_news': News.objects.count(),
        'published_news': News.objects.filter(published=True).count(),
        'total_events': Event.objects.count(),
        'published_events': Event.objects.filter(published=True).count(),
        'total_testimonials': Testimonial.objects.count(),
        'approved_testimonials': Testimonial.objects.filter(approved=True).count(),
        'pending_testimonials': Testimonial.objects.filter(approved=False).count(),
        'total_campus_images': CampusLife.objects.count(),
        'published_campus_images': CampusLife.objects.filter(published=True).count(),
        'total_contact_messages': ContactMessage.objects.count(),
        'unread_messages': ContactMessage.objects.filter(read=False).count(),
        'unreplied_messages': ContactMessage.objects.filter(replied=False).count(),
    })