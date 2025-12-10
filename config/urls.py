from rest_framework import routers
from django.urls import path, include
from users.views import UserViewSet, StudentProfileViewSet, stats
from academics.views import CourseViewSet, AssignmentViewSet, EnrollmentViewSet, SubmissionViewSet
from communication.views import AnnouncementViewSet, NotificationViewSet
from communication.views import ContactMessageCreateView
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
router.register(r'announcements', AnnouncementViewSet)
router.register(r'notifications', NotificationViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('stats/', stats, name='stats'),
    path("contact/", ContactMessageCreateView.as_view(), name="contact-create"),
]
