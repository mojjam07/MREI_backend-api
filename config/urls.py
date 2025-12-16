

from rest_framework import routers
from django.urls import path, include
from users.views import UserViewSet, StudentProfileViewSet, RegisterView, stats, CustomTokenObtainPairView, CurrentUserView
from academics.views import (
    CourseViewSet, AssignmentViewSet, EnrollmentViewSet, AssignmentSubmissionViewSet,
    ClassScheduleViewSet, AttendanceViewSet,
    TutorDashboardView, StudentDashboardView, AdminDashboardView,
    AdminTutorManagementView, AdminStudentManagementView
)


from communication.views import StatisticsViewSet, NewsViewSet, EventViewSet, TestimonialViewSet, CampusLifeViewSet, ContactMessageViewSet, BookViewSet, get_home_content, dashboard_stats, global_search, quick_search
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
router.register(r'submissions', AssignmentSubmissionViewSet, basename='submissions')
router.register(r'class-schedules', ClassScheduleViewSet, basename='class-schedules')
router.register(r'attendance', AttendanceViewSet)
router.register(r'statistics', StatisticsViewSet, basename='statistics')
router.register(r'news', NewsViewSet, basename='news')
router.register(r'events', EventViewSet, basename='events')
router.register(r'testimonials', TestimonialViewSet, basename='testimonials')
router.register(r'campus-life', CampusLifeViewSet, basename='campus-life')
router.register(r'contact', ContactMessageViewSet, basename='contact')
router.register(r'books', BookViewSet, basename='books')




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
    
    # Dashboard Analytics Endpoints
    path('dashboard/tutor/', TutorDashboardView.as_view(), name='tutor_dashboard'),
    path('dashboard/student/', StudentDashboardView.as_view(), name='student_dashboard'),
    path('dashboard/admin/', AdminDashboardView.as_view(), name='admin_dashboard'),
    

    # Admin Management Endpoints
    path('admin/tutors/', AdminTutorManagementView.as_view(), name='admin_tutors'),
    path('admin/students/', AdminStudentManagementView.as_view(), name='admin_students'),
    
    # Search Endpoints
    path('search/global/', global_search, name='global_search'),
    path('search/quick/', quick_search, name='quick_search'),
]
