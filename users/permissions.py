
# users/permissions.py
from rest_framework import permissions


class IsTutor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'tutor'


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'student'


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class RoleBasedPermission(permissions.BasePermission):
    """Permission that checks if user has required roles"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        required_roles = getattr(view, 'required_roles', [])
        if not required_roles:
            return True
        
        return request.user.role in required_roles


class IsOwnerOrAdmin(permissions.BasePermission):
    """Object-level permission that allows owners or admins to edit"""
    
    def has_object_permission(self, request, view, obj):
        # Admin can edit everything
        if request.user.role == 'admin':
            return True
        
        # Owner can edit their own objects
        if hasattr(obj, 'user') and obj.user == request.user:
            return True
        if hasattr(obj, 'student') and obj.student == request.user:
            return True
        if hasattr(obj, 'tutor') and obj.tutor == request.user:
            return True
        if hasattr(obj, 'sender') and obj.sender == request.user:
            return True
        if hasattr(obj, 'receiver') and obj.receiver == request.user:
            return True
            
        return False


class IsTutorOfStudent(permissions.BasePermission):
    """Permission for tutors to access their assigned students' data"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated or request.user.role != 'tutor':
            return False
        
        # Check if tutor has assignments with students
        from academics.models import AdminTutorAssignment, Enrollment
        from django.db.models import Q
        
        # Get students enrolled in tutor's courses
        student_ids = Enrollment.objects.filter(
            course__tutor=request.user,
            status='enrolled'
        ).values_list('student_id', flat=True)
        
        return student_ids.exists()


class IsAdminOfUser(permissions.BasePermission):
    """Permission for admins to access users they manage"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated or request.user.role != 'admin':
            return False
        
        return True  # Admins can access all user data


class IsEnrolledInCourse(permissions.BasePermission):
    """Permission for students to access their enrolled courses"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated or request.user.role != 'student':
            return False
        
        return True  # Students can access their own course data
    
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'student') and obj.student != request.user:
            return False
        
        if hasattr(obj, 'course') and request.user.role == 'student':
            from academics.models import Enrollment
            return Enrollment.objects.filter(
                student=request.user,
                course=obj.course,
                status='enrolled'
            ).exists()
        
        return True
