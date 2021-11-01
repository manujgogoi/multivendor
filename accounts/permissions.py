from rest_framework import permissions

class IsAdminAndSelfOrReadonly(permissions.BasePermission):
    '''
    Custom permission to only admin (staff) and self
    have write access.
    '''
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if request.user.is_staff:
            return True

        if request.user == obj:
            return True
        return False