from rest_framework import permissions

class IsStaffOrNone(permissions.BasePermission):
    '''
    Custom permission to only allow staff users
    to view users list
    '''


    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        elif request.user.is_staff:
            if request.method in permissions.SAFE_METHODS:
                return True 
        if request.user == obj:
            return True
        return False