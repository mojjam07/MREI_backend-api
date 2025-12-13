
from rest_framework import routers
from django.urls import path, include
from users.views import UserViewSet, StudentProfileViewSet, RegisterView, stats, CustomTokenObtainPairView, CurrentUserView
from academics.views import CourseViewSet, AssignmentViewSet, EnrollmentViewSet, SubmissionViewSet
from communication.views import StatisticsViewSet, NewsViewSet, EventViewSet, TestimonialViewSet, CampusLifeViewSet, ContactMessageViewSet, get_home_content, dashboard_stats
# from communication.views import ContactMessageCreateView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'students', StudentProfileViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'enrollments', EnrollmentViewSet)
router.register(r'assignments', AssignmentViewSet)
router.register(r'submissions', SubmissionViewSet)
router.register(r'statistics', StatisticsViewSet, basename='statistics')
router.register(r'news', NewsViewSet, basename='news')
router.register(r'events', EventViewSet, basename='events')
router.register(r'testimonials', TestimonialViewSet, basename='testimonials')
router.register(r'campus-life', CampusLifeViewSet, basename='campus-life')
router.register(r'contact', ContactMessageViewSet, basename='contact')



urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Add endpoint for getting current user data
    path('auth/user/', CurrentUserView.as_view(), name='current_user'),
    path('stats/', stats, name='stats'),
    path('home-content/', get_home_content, name='home-content'),
    path('dashboard-stats/', dashboard_stats, name='dashboard-stats'),
]
