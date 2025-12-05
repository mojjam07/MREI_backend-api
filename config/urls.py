from rest_framework import routers
from django.urls import path, include
from users.views import UserViewSet, StudentProfileViewSet
from academics.views import CourseViewSet, AssignmentViewSet, EnrollmentViewSet, SubmissionViewSet
from communication.views import AnnouncementViewSet, NotificationViewSet


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
path('api/', include(router.urls)),
path('api/auth/', include('rest_framework_simplejwt.urls')),
]